$(document).ready(function () {

    var max_limit = parseInt($("#max-limit").text());

    /**
     * Generate UUID for poll
     */
    function create_UUID() {
        var dt = new Date().getTime();
        var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = (dt + Math.random() * 16) % 16 | 0;
            dt = Math.floor(dt / 16);
            return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
        return uuid;
    }

    function setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }

    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }

    function checkCookie() {
        var uuid = getCookie("uuid");
        if (uuid != "") {
            console.log(uuid);
        } else {
            uuid = create_UUID();
            if (uuid != "" && uuid != null) {
                setCookie("uuid", uuid, 365);
            }
        }
    }

    // Check whether cookie is exist, if not then create one
    checkCookie();

    // Form validation
    $("#poll-form").on("submit", function (e) {
        var arr = $(this).serialize().toString();
        if (arr.indexOf("answer") < 0) {
            // No answer selected
            e.preventDefault();
            $(".answer-selection").addClass("is-invalid");
            $(".invalid-feedback").text("At least choose one answer");
        } else if ($(".answer-selection:checked").length > max_limit) {
            // Select more than max limit
            e.preventDefault();
            $(".answer-selection").addClass("is-invalid");
            $(".invalid-feedback").text("You can only select up to " + max_limit + " options");
        } else {
            var uuid = getCookie("uuid");
            if (uuid === "") {
                uuid = create_UUID();
            }
            $(this).find("input[name=" + "uuid" + "]").remove();
            $("<input />").attr("type", "hidden")
                .attr("name", "uuid")
                .attr("value", uuid)
                .appendTo("#poll-form");
        }
    });

    $(".answer-selection").change(function () {
        console.log($(".answer-selection:checked").length);
    });
});