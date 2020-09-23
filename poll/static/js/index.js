$(document).ready(function () {

    var maxSelectionLimit = 2;

    /**
     * Set maximum selection limit
     */
    const setMaxSelectionLimit = (limit) => {
        $('#max-selection-limit').attr('max', limit);

        // If current max selections limit is greater than limit
        // then set it to the new limit
        if ($('#max-selection-limit').val() > limit) {
            $('#max-selection-limit').val(limit);
        }
    };

    // The HTML template of answer input box
    const AnswerTemplate = () => `
        <div class="input-group added-answer-root mb-2">
            <input name="answer" type="text" required="required" class="form-control" maxlength="255"
                placeholder="Type your answer" value="">
            <div class="input-group-append">
                <button class="btn btn-sm btn-outline-danger remove-answer-button" type="button">
                    <svg width="18" height="18" viewBox="0 0 16 16" class="bi bi-x"
                        fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd"
                        d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z" />
                    </svg>
                </button>
            </div>
        </div>
    `;

    /**
     * Add an answer when the button is clicked
     */
    $('#add-answer-button').click(function () {
        $('#poll-answers').append( AnswerTemplate );
        maxSelectionLimit += 1;
        setMaxSelectionLimit(maxSelectionLimit);
        console.log(maxSelectionLimit);
    });

    /**
     * Delete the answer of the clicked button belonged
     */
    $('#poll-answers').on("click", ".remove-answer-button", function() {
        $( this ).parents( ".added-answer-root" ).remove();
        maxSelectionLimit -= 1;
        setMaxSelectionLimit(maxSelectionLimit);
        console.log(maxSelectionLimit);
    });
});