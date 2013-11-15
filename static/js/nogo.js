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

    // Behavior on change of Field (enable next field)
    organism_accessor.change(fieldUpdated);
    branch_accessor.change(fieldUpdated);
    term_accessor.change(fieldUpdated);
    algorithms_accessor.change(algorithmUpdated);

    function fieldUpdated(e) {
        updateButton();
        updateFigure();
    }

    function algorithmUpdated(e) {
        updateButton();
    }

    // Behavior on form submit
    form_accessor.submit(function (e) {
        // If all values are populated, display patience and submit form (return true)
        if (allFieldsSet() && algorithmSelected()) {
            setDownloadMessage("Please be patient - this may take a minute (fewer algorithm selections reduces time)");
            return true;
        }
        // If not, alert re: missing selections and prevent form submission (return false)
        else  {
            alert("Must select a value for all fields and at least one algorithm!");
            return false;
        }
    });


    // Utility functions
    function allFieldsSet() {
        var fields = getGoFieldValues();
        if (fields["organism"] != "" && fields["branch"] != "" && fields["term"] != "") {
            return true;
        }
        return false;
    }

    function algorithmSelected() {
        var algorithms = getAlgorithmValues();
        if (algorithms["rocchio"] || algorithms["netl"] || algorithms["snob"]) {
            return true;
        }
        return false;
    }

    function updateButton() {
        if (allFieldsSet() && algorithmSelected()) {
            button_accessor.removeAttr("disabled");
            return;  
        }
        button_accessor.attr("disabled", "disabled");
    }

    function updateFigure(organism, branch, term) {
        var figure_ref = FigureLocation;
        var fields = getGoFieldValues();
        var organism = fields["organism"];
        var branch = fields["branch"];
        var term = fields["term"];

        setFigureMessage("");

        if (organism == "") {
            setFigureSource(DefaultFigure);
            setFigureMessage(FigureCaption);
            return;
        }
        else if (branch == "") {
            figure_ref += organism + ".png";
            setFigureSource(figure_ref);
            setFigureMessage(FigureCaption);
            return;
        }
        else if (term == "") {
            figure_ref += organism + "_" + branch + ".png";
            setFigureSource(figure_ref);
            setFigureMessage(FigureCaption);
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
                        setFigureMessage(FigureCaption);
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

    // On page load (here), call functions to initialize page
    setDownloadMessage("");
    setFigureMessage(FigureCaption);

 })
