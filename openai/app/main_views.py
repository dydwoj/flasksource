from flask import url_for, render_template, request
from flask import Blueprint
from dotenv import load_dotenv
from openai import OpenAI
from .forms import AdCommentForm
from googletrans import Translator
import deepl
import os
import asyncio

# .env load
load_dotenv()

client = OpenAI()
Model = "gpt-4o-mini"

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
    # role_content = """ 당신은 텍스트를 한국어로 요약하는 전문가입니다.
    # - 당신의 임무는 아래 주어진 텍스트 문장을 한국어로 요약하는 것입니다.
    # - 요약시, 다음 사항을 반드시 반영해야 합니다.
    #     - 중복된 내용은 생략하되, 반복되는 내용은 요약에서 더 강조합니다.
    #     - 사례 중심보다는 개념과 주장 중심으로 요약합니다.
    #     - 3줄 이내로 요약합니다.
    #     - 불릿 기호(*) 형식으로 작성합니다.
    # """

    role_content = """당신은 최고의 번역가입니다.
    사용자가 제시하는 문장을 한국어로 번역해 주세요
    """

    message_prompt = [
        {"role": "developer", "content": role_content},
    ]
    message_prompt.append(prompt)

    response = client.chat.completions.create(
        model=Model,
        messages=message_prompt,
    )

    return response.choices[0].message.content


@bp.route("/ad", methods=["GET", "POST"])
def ad():
    form = AdCommentForm()

    if request.method == "POST" and form.validate_on_submit():
        text = f"""
        - 제품명 : {form.name.data}
        - 브랜드명 : {form.brand.data}
        - 제품특징 : {form.strength.data}
        - 톤엔매너 : {form.tone.data}
        - 필수포함키워드 : {form.keyword.data}
        - 브랜드핵심가치 : {form.value.data}
        """

        prompt = {"role": "user", "content": text}

        ad_result = ask_gpt(prompt)
        return render_template("ad.html", form=form, ad_result=ad_result)

    return render_template("ad.html", form=form)


@bp.route("/summarize", methods=["GET", "POST"])
def summarize():

    if request.method == "POST":

        # 사용자가 입력한 내용 가져오기
        text = request.form.get("text")

        prompt = {"role": "user", "content": text}

        summarize_result = ask_gpt(prompt)
        return render_template(
            "summarize.html", summarize_result=summarize_result, text=text
        )

    return render_template("summarize.html")


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
