$(document).ready(function () {

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

    checkCookie();

    $("#poll-form").on("submit", function (e) {
        var arr = $(this).serialize().toString();
        if (arr.indexOf("answer") < 0) {
            e.preventDefault();
            $(".answer-selection").addClass("is-invalid");
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
        if (this.checked) {
            $(".answer-selection").removeClass("is-invalid");
        }
    });
});