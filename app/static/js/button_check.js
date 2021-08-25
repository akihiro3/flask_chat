$(".talk").click(function () {
    if ($(".in_form").val()) {
        $(this).prop("disabled", true);
        $(this).closest("form").submit();
    }
});


$(function () {
    let target = document.getElementById('scroll-inner');
    target.scrollIntoView(false);
});