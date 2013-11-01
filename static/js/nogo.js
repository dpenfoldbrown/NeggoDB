/* 
 * Javascript functions for NoGO website
 * @auth dpb
 * @date 10/24/2013
 */

 $(function() {

    // Get frontpage elements as jquery accessors, vars to reduce redundancy of hard coding
    var organism_accessor = $("#f_organism");
    var branch_accessor = $("#f_branch");
    var term_accessor = $("#f_goterm");
    var algorithms_accessor = $(".f_algorithm");
    var button_accessor = $("#f_download");

    // Behavior on change of Organism select box (enable GO Branch select box)
    organism_accessor.change(setBranchField);

    // Behavior on change of GO Branch select box (enable GO Term input)
    branch_accessor.change(setTermField);

    // Behavior on change of GO Term input box (enable Algorithm checkboxes)
    term_accessor.change(setAlgorithmsField);

    // Behavior on change of Algorithm checkboxes (enable download button if disabled)
    algorithms_accessor.change(setButtonField);


    function setBranchField(e) {
        if (organism_accessor.val() == "") {
            branch_accessor.attr("disabled", "disabled");
            return;
        }
        branch_accessor.removeAttr("disabled");

        //TODO: Change image to loader, Check value, Change image to pre-gen chart
        //TODO: (build image href file string by getting field vals)
    }
    
    function setTermField(e) {
        if (branch_accessor.val() == "") {
            term_accessor.attr("disabled", "disabled");
            return;
        }
        term_accessor.removeAttr("disabled");

        //TODO: Change image to loader, Check value, Change image to pre-gen chart
        //TODO: (build image href file string by getting field vals)
    }
    
    function setAlgorithmsField(e) {
        if (term_accessor.val() == "") {
            algorithms_accessor.attr("disabled", "disabled");
            return;
        }
        algorithms_accessor.removeAttr("disabled");

        //TODO: Change image to loader, get Org, Branch, and Term values, and send AJAX request to
        //TODO: server with those fields. On success response, change image to returned file href.
        //TODO: on error response, switch img back to original frontpage and display error message.
    }
    
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

    //TODO: On Form submit (capture form submit - better than click event on button), show loader 
    //TODO: and "please wait message" (page will reload on server response, but that may take a
    //TODO: while due to file gen.)


    // // Behavior on Download button click
    // function requestData(e) {
    //     // Get all values
    //     var org = organism_accessor.val();
    //     var branch = branch_accessor.val();
    //     var term = term_accessor.val();
    //
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
    setBranchField();
    setTermField();
    setAlgorithmsField();
    setButtonField();

 })
