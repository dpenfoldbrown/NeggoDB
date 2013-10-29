/* 
 * Javascript functions for NoGO website
 * @auth dpb
 * @date 10/24/2013
 */

 $(function() {

    // TODO: Define click() of button: check if disabled. If so, alert warning about selection.
    // TODO: Otherwise, send AJAX to server-side with file request. Don't wait for response - server
    // TODO: side will send a mimetype file download thing.

    // Get frontpage elements as jquery accessors, vars to reduce redundancy of hard coding
    var org_accessor = $("#f_organism");
    var branch_accessor = $("#f_branch");
    var term_accessor = $("#f_goterm");
    var algs_accessor = $(".f_algorithm");
    var button_accessor = $("#f_download");

    // Behavior on change of Organism select box (enable GO Branch select box)
    function setBranchField(e) {
        if (org_accessor.val() == "") {
            branch_accessor.attr("disabled", "disabled");
            return;
        }
        branch_accessor.removeAttr("disabled");

        //TODO: Change image with loader, Check value, Change image to pre-gen chart
    }
    org_accessor.change(setBranchField);


    // Behavior on change of GO Branch select box (enable GO Term input)
    function setTermField(e) {
        if (branch_accessor.val() == "") {
            term_accessor.attr("disabled", "disabled");
            return;
        }
        term_accessor.removeAttr("disabled");

        //TODO: Change image with loader, Check value, Change image to pre-gen chart
    }
    branch_accessor.change(setTermField);


    // Behavior on change of GO Term input box (enable Algorithm checkboxes)
    function setAlgorithmsField(e) {
        if (term_accessor.val() == "") {
            algs_accessor.attr("disabled", "disabled");
            return;
        }
        algs_accessor.removeAttr("disabled");

        //TODO: Change image with loader, Send AJAX request with params, When return recv'd, set image to returned href
    }
    term_accessor.change(setAlgorithmsField);


    // Behavior on change of Algorithm checkboxes (enable download button if disabled)
    function setButtonField(e) {
        var rocc_selected = $("#alg_rocc").is(':checked');
        var netl_selected = $("#alg_netl").is(':checked');
        var snob_selected = $("#alg_snob").is(':checked');

        if (rocc_selected || netl_selected || snob_selected) {
            button_accessor.removeAttr("disabled");
        } else {
            button_accessor.attr("disabled", "disabled");
        }
    }
    algs_accessor.change(setButtonField);


    // // Behavior on Download button click
    // function requestData(e) {
    //     // Get all values
    //     var org = org_accessor.val();
    //     var branch = branch_accessor.val();
    //     var term = term_accessor.val();
    //     var rocc = $("#alg_rocc").is(':checked');
    //     var netl = $("#alg_netl").is(':checked');
    //     var snob = $("#alg_snob").is(':checked');

    //     // Check all values, alert if no good
    //     if (org == "" || org == null) { 
    //         alert("Error: Must select an organism");
    //         return;
    //     }
    //     if (branch == "" || branch == null) { 
    //         alert("Error: Must select a GO Branch"); 
    //         return;
    //     }
    //     if (term == "" || term == null) { 
    //         alert("Error: Must enter a GO Term"); 
    //         return;
    //     }
    //     if (!(rocc || netl || snob)) { 
    //         alert("Error: Must select at least one Algorithm") 
    //         return;
    //     }

    //     // Make an AJAX Post call to server with input field values
    //     var jqxhr = $.post("/NoGO/data",
    //         {
    //             "organism": org,
    //             "branch": branch,
    //             "go_term": term,
    //             "rocchio": rocc,
    //             "netl": netl,
    //             "snob": snob
    //         },
    //         function (data) {
    //             console.log("jQuery Post call success. Data: ");
    //             console.log(data);
    //         }).done( function() {
    //             console.log("jQuery Post done");
    //         }).fail( function() {
    //             console.log("jQuery Post failed");
    //         }).always( function() {
    //             console.log("jQuery Post always");
    //         });

    // }
    // button_accessor.click(requestData)


    // On page load (here), call all functions to make sure of correct enable/disable scheme
    setBranchField(null);
    setTermField(null);
    setAlgorithmsField(null);
    setButtonField(null);

 })
