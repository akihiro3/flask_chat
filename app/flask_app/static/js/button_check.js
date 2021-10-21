let text_form = document.getElementById('in_form');
let targetButtonId = document.getElementById('talk');

text_form.addEventListener('keypress', test_event);

//エンターキーを押された時も送信する
function test_event(e) {
    let val;
    if (!(text_form.value) || text_form.value === '\n') {
        text_form.value = null;
        return false;
    } else {
        if (e.key === "Enter") {
            targetButtonId.click();
            return false;
        } else {
            return false;
        }
    }

}

//チャット画面の一番下までスクロールする
window.onload = function () {
    const target = document.getElementById('scroll-inner');
    target.scrollIntoView(false);
}