/* 
 * Javascript functions for NoGO website
 * @auth dpb
 * @date 10/24/2013
 */

 $(function() {

    // Config variables
    var FigureLocation = "static/img/pregenerated/";
    var DefaultFigure = "static/img/pregenerated/sample01.png";
    var LoadingImg = "static/img/loader.gif";
    var ErrorImg = "static/img/error.png";


    // Get frontpage elements as jquery accessors, vars to reduce redundancy of hard coding
    var organism_accessor = $("#f_organism");
    var branch_accessor = $("#f_branch");
    var term_accessor = $("#f_goterm");
    var algorithms_accessor = $(".f_algorithm");
    var button_accessor = $("#f_download");

    var figure_accessor = $("#selection-fig");
    var figure_link_accessor = $("#selection-fig-link");


    // Behavior on change of Field (enable next field)
    organism_accessor.change(setBranchField);
    branch_accessor.change(setTermField);
    term_accessor.change(setAlgorithmsField);
    algorithms_accessor.change(setButtonField);


    function makeFigureHref(organism, branch) {
        var figure_ref = FigureLocation;
        
        if (organism == "") {
            return DefaultFigure;
        } else {
            figure_ref += organism;
        }
        if (branch != "") {
            figure_ref += "_" + branch;
        }
        figure_ref += ".png"
        return figure_ref
    }

    function setFigureSource(figure_ref) {
        figure_accessor.attr("src", figure_ref);
        figure_link_accessor.attr("href", figure_ref);
    }

    function getGoFieldValues() {
        return {
            "organism": organism_accessor.val(),
            "branch": branch_accessor.val(),
            "term": term_accessor.val()
        };   
    }

    function getAlgorithmValues() {
        return {
            "rocchio": $("#alg_rocc").is(':checked'),
            "netl": $("#alg_netl").is(':checked'),
            "snob": $("#alg_snob").is(':checked')
        };
    }

    function setBranchField(e) {
        var figure_ref;
        var goFields = getGoFieldValues();
        if (goFields["organism"] == "") {
            branch_accessor.attr("disabled", "disabled");
        }
        else {
            branch_accessor.removeAttr("disabled");
            figure_ref = makeFigureHref(goFields["organism"], goFields["branch"]);
            setFigureSource(figure_ref);
        }
    }
    
    function setTermField(e) {
        var figure_ref;
        var goFields = getGoFieldValues();
        if (goFields["branch"] == "") {
            term_accessor.attr("disabled", "disabled");
        } else {
            term_accessor.removeAttr("disabled");
            figure_ref = makeFigureHref(goFields["organism"], goFields["branch"]);
            setFigureSource(figure_ref);
        }
    }
    
    function setAlgorithmsField(e) {
        var figure_ref;
        var goFields = getGoFieldValues();

        if (goFields["term"] == "") {
            algorithms_accessor.attr("disabled", "disabled");
        }
        else {
            algorithms_accessor.removeAttr("disabled");
            setFigureSource(LoadingImg);
        }

        //TODO: Send AJAX request to server with values. On success response, change image to returned file href.
        //TODO: on error response, switch img back to original frontpage and display error message.

        // figure_ref = AJAX CALL RETURN, check if success
        // setFigureSource(figure_ref);
    }
    
    function setButtonField(e) {
        algorithms = getAlgorithmValues();

        if (algorithms["rocchio"] || algorithms["netl"] || algorithms["snob"]) {
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
