// 삭제버튼 클릭시 confirm("정말 삭제하시겠습니까?") 띄우기

const elements = document.querySelectorAll(".delete");

elements.forEach((ele) => {
  ele.addEventListener("click", (e) => {
    e.preventDefault();
    const href = e.target.getAttribute("href");
    console.log(href);

    if (confirm("정말 삭제하시곘습니까?")) {
      location.href = href;
    }
  });
});
