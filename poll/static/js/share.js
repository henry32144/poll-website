$(document).ready(function () {

    function selectAndCopy(id) {
        var copyText = document.getElementById(id);

        /* Select the text field */
        copyText.select();
        copyText.setSelectionRange(0, 99999); /*For mobile devices*/

        /* Copy the text inside the text field */
        document.execCommand("copy");
    }

    $('.popover-button').popover({
        trigger: 'click'
    })

    $('.popover-button').on('shown.bs.popover', function () {
        setTimeout(function () {
            $(".popover-button").popover('hide')
        }, 2000);
    })

    $('#share-link-button').on("click", function () {
        selectAndCopy('share-link-box');
    });

    $('#modify-link-button').on("click", function () {
        selectAndCopy('modify-link-box');
    });
});