let text_form = document.getElementById('in_form');
let targetButtonId = document.getElementById('talk');

text_form.addEventListener('keypress', test_event);

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

window.onload = function () {
    const target = document.getElementById('scroll-inner');
    target.scrollIntoView(false);
}