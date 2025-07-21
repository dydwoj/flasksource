from flask import flash, render_template, request
from flask import Blueprint
from dotenv import load_dotenv
from openai import OpenAI
from .forms import AdCommentForm
from googletrans import Translator
import deepl
import os
import asyncio

# pdf 라이브러리
from PyPDF2 import PdfReader
from langchain.chains.question_answering import load_qa_chain

# 텍스트 분리
from langchain.text_splitter import CharacterTextSplitter

# OpenAI
from langchain_openai import ChatOpenAI

from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# .env load
load_dotenv()

Model = "gpt-4o-mini"
client = OpenAI()

bp = Blueprint("main", __name__, url_prefix="/")


async def ask_google(prompt):
    async with Translator() as translator:
        result = await translator.translate(prompt, dest="ko")
        return result.text


def ask_deepl(prompt):
    DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
    translator = deepl.Translator(DEEPL_API_KEY)
    result = translator.translate_text(prompt, target_lang="ko")
    return result.text


def ask_gpt(prompt):
    #     role_content = """당신은 텍스트를 한국어로 요약하는 전문가입니다.
    # - 당신의 임무는 아래 주어진 텍스트 문장을 한국어로 요약하는 것입니다.
    # - 요약 시 다음 사항을 반드시 반영해야 합니다.
    #     - 중복된 내용은 생략하되, 반복되는 내용은 요약에서 더 강조합니다.
    #     - 사례 중심보다는 개념과 주장 중심으로 요약합니다.
    #     - 3줄 이내로 요약합니다.
    #     - 불릿 기호(*) 형식으로 작성합니다.
    # """

    role_content = """당신은 최고의 번역가입니다.
    사용자가 제시하는 문장을 한국어로 번역해 주세요
    """

    message_prompt = [{"role": "developer", "content": role_content}]
    message_prompt.append(prompt)

    response = client.chat.completions.create(
        model=Model,
        messages=message_prompt,
    )

    return response.choices[0].message.content


def pdf_text_extract(upload_file):
    """
    pdf 파일에서 text 추출
    """
    reader = PdfReader(upload_file)

    total_text = ""
    for page in reader.pages:
        total_text += page.extract_text()
    return total_text


def chunk_split(total_text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(total_text)
    return chunks


def embedding_extract(chunks):
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    return knowledge_base


@bp.route("/pdf", methods=["GET", "POST"])
def pdf():

    if request.method == "POST":
        # 사용자가 업로드한 pdf 가져오기
        file = request.files.get("file")
        # 사용자 질문 가져오기
        question = request.form.get("question")

        if not file:
            return flash("파일 업로드 확인")

        # 1. pdf 텍스트 추출
        total_text = pdf_text_extract(file)
        # 2. 텍스트 분할
        chunks = chunk_split(total_text)
        # 3. 임베딩 처리
        knowledge_base = embedding_extract(chunks)
        # 4. GPT 모델과 랭체인 연동
        lim = ChatOpenAI(
            temperature=0,
            max_completion_tokens=3000,
            model_name=Model,
            request_timeout=120,
        )
        chain = load_qa_chain(lim, chain_type="stuff")
        # 5. 유사도를 이용해 질문과 유사한 문서 추출
        docs = knowledge_base.similarity_search(question)
        # 6. 질문하기
        output = chain.invoke({"input_documents": docs, "question": question})
        # 7. 번역하기
        result = asyncio.run(ask_google(output["output_text"]))

        return render_template("pdf.html", question=question, result=result)

    return render_template("pdf.html")


@bp.route("/trans", methods=["GET", "POST"])
def trans():

    if request.method == "POST":
        # 사용자가 입력한 내용 가져오기
        text = request.form.get("text")

        prompt = {"role": "user", "content": text}
        trans_gpt = ask_gpt(prompt)
        trans_google = asyncio.run(ask_google(text))
        trans_deepl = ask_deepl(text)

        return render_template(
            "trans.html",
            openai=trans_gpt,
            google=trans_google,
            deepl=trans_deepl,
            text=text,
        )

    return render_template("trans.html")


@bp.route("/ad", methods=["GET", "POST"])
def ad():
    form = AdCommentForm()

    if request.method == "POST" and form.validate_on_submit():
        # 사용자가 입력한 내용 가져오기
        text = f"""
        - 제품명 : {form.name.data}
        - 브랜드명 : {form.brand.data}
        - 브랜드 핵심 가치 : {form.value.data}
        - 제품특징 : {form.strenghth.data}
        - 톤엔 매너 : {form.tone.data}
        - 필수 포함 키워드 : {form.keyword.data}
        """

        prompt = {"role": "user", "content": text}
        ad_result = ask_gpt(prompt)
        return render_template("ad.html", form=form, ad_result=ad_result)

    return render_template("ad.html", form=form)


@bp.route("/summerize", methods=["GET", "POST"])
def summerize():

    if request.method == "POST":
        # 사용자가 입력한 내용 가져오기
        text = request.form.get("text")

        prompt = {"role": "user", "content": text}
        summerize_result = ask_gpt(prompt)
        return render_template(
            "summerize.html", summerize_result=summerize_result, text=text
        )

    return render_template("summerize.html")
