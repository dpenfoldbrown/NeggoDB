/* 
 * Javascript functions for NoGO website
 * @auth dpb
 * @date 10/24/2013
 */

 $(function() {

    // Config variables
    var FigureLocation = "static/img/pregenerated/";
    var DefaultFigure = "static/img/pregenerated/AllOrganismAverage.png";
    var LoadingImg = "static/img/loader.gif";
    var ErrorImg = "static/img/error.png";
    var FigureCaption = "This plot depicts the number of incorrectly predicted negative examples as a function of the number of negative examples chosen. A lower value indicates an algorithm with better performance, with the dashed blue line serving as a reference (the number of incorrectly predicted negative examples if negative examples were selected at random)";

    // Get frontpage elements as jquery accessors, vars to reduce redundancy of hard coding
    var organism_accessor = $("#f_organism");
    var branch_accessor = $("#f_branch");
    var term_accessor = $("#f_goterm");
    var algorithms_accessor = $(".f_algorithm");
    var button_accessor = $("#f_download");

    var figure_accessor = $("#selection-fig");
    var figure_link_accessor = $("#selection-fig-link");
    var form_accessor = $("#download-form");

    // Setter functions
    function setDownloadMessage(message) {
       $("#download-message").text(message); 
    }
    function setFigureMessage(message) {
        $("#figure-message").text(message);
    }
    function setFigureSource(figure_ref) {
        figure_accessor.attr("src", figure_ref);
        figure_link_accessor.attr("href", figure_ref);
    }

    // Getter functions
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


    // Behavior on change of Field (enable next field)
    organism_accessor.change(setBranchField);
    branch_accessor.change(setTermField);
    term_accessor.change(setAlgorithmsField);
    algorithms_accessor.change(setButtonField);

    // Behavior on form submit (don't prevent default)
    form_accessor.submit(function (e) {
        setDownloadMessage("Please be patient - this may take a minute (fewer algorithm selections reduces time)");
    });

    // Utility functions
    function updateFigure(organism, branch, term) {
        var figure_ref = FigureLocation;

        if (organism == "") {
            setFigureSource(DefaultFigure);
        }
        else if (branch == "") {
            figure_ref += organism + ".png";
            setFigureSource(figure_ref);
            return;
        }
        else if (term == "") {
            figure_ref += organism + "_" + branch + ".png";
            setFigureSource(figure_ref);
            return;
        }
        else {
            // Request image creation
            setFigureSource(LoadingImg);
            
            // Send AJAX request to server with form values, setting images as return indicates
            var jqxhr = $.post(
                "/figure",
                {
                    "Organism": organism,
                    "Branch": branch,
                    "Term": term
                },
                function(data) {
                    // Return data format: { "code": ..., "message": ..., "file_href": ...}
                    console.log(data);

                    if (data["code"] == "OK") {
                        // On success response, change image to returned file href
                        setFigureSource(data["file_href"]);
                    }
                    else {
                        // On error response, switch img back to original frontpage and display 
                        // error message.
                        setFigureSource(ErrorImg);
                        setFigureMessage(data["message"]);
                    }
                }).fail( function() {
                    // On AJAX POST failure, displasy error image and message
                    setFigureSource(ErrorImg);
                    setFigureMessage("Error communicating with server. No image to be set :-(");
                });
        }
    }

    // Field-set handlers
    function setBranchField(e) {
        var figure_ref;
        var goFields = getGoFieldValues();
        if (goFields["organism"] == "") {
            branch_accessor.attr("disabled", "disabled");
        }
        else {
            branch_accessor.removeAttr("disabled");
        }
        updateFigure(goFields["organism"], goFields["branch"], goFields["term"]);
    }
    
    function setTermField(e) {
        var figure_ref;
        var goFields = getGoFieldValues();
        if (goFields["branch"] == "") {
            term_accessor.attr("disabled", "disabled");
        } else {
            term_accessor.removeAttr("disabled");
        }
        updateFigure(goFields["organism"], goFields["branch"], goFields["term"]);
    }
    
    function setAlgorithmsField(e) {
        var figure_ref;
        var goFields = getGoFieldValues();
        if (goFields["term"] == "") {
            algorithms_accessor.attr("disabled", "disabled");
        }
        else {
            algorithms_accessor.removeAttr("disabled");
            updateFigure(goFields["organism"], goFields["branch"], goFields["term"]);
        }
    }
    
    function setButtonField(e) {
        algorithms = getAlgorithmValues();
        if (algorithms["rocchio"] || algorithms["netl"] || algorithms["snob"]) {
            button_accessor.removeAttr("disabled");
        } else {
            button_accessor.attr("disabled", "disabled");
        }
    }

    // On page load (here), call all functions to make sure of correct enable/disable and figure scheme
    setDownloadMessage("");
    setFigureMessage(FigureCaption);
    setBranchField();
    setTermField();
    setAlgorithmsField();
    setButtonField();

 })
