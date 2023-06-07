
function removeOptions(selectbox_id) {
    let selectbox = document.getElementById(selectbox_id);
    var i, L = selectbox.options.length - 1;
    for (i = L; i > 0; i--) {
        selectbox.remove(i);
    }
}

function resolve_variables(k){
    let input_id, results_id, url;
    let city = "", state = "", country = "";
    if (k == 0) {
        input_id = "country_name";
        results_id = "country_results";
        url = "/search-country?country=";
        removeOptions("state_results");
        removeOptions("city_results");
    } else if (k == 1) {
        if(document.getElementById("country_name")){
            country = document.getElementById("country_name").value.toLowerCase();
        }
        input_id = "state_name";
        results_id = "state_results";
        url = "/search-state?country="+country+"&state=";
        removeOptions("city_results");
    } else if (k == 2) {
        if(document.getElementById("country_name")){
            country = document.getElementById("country_name").value.toLowerCase();
        }
        if(document.getElementById("state_name")){
            state = document.getElementById("state_name").value.toLowerCase().split(',')[0];
        }
        input_id = "city_name";
        results_id = "city_results";
        url = "/search-city?country="+country+"&state="+state+"&city=";
    } else if (k == 3){
        if(document.getElementById("city_name")){
            city = document.getElementById("city_name").value.toLowerCase();
        }
        input_id = "airport_code";
        results_id = "airport_results";
        url = "/search-airport?country="+country+"&state="+state+"&city="+city+"&airport=";
    }
    else if(k == 4){
        input_id = "source_city_name";
        results_id = "source_city_results";
        url = "/search-city?country="+country+"&state="+state+"&city=";

    }
    else if(k == 5){
        input_id = "destination_city_name";
        results_id = "destination_city_results";
        url = "/search-city?country="+country+"&state="+state+"&city=";
    }
    else if(k == 6){
        if (document.getElementById("source_city_name")) {
            city = document.getElementById("source_city_name").value.toLowerCase();
        }
        input_id = "source_airport_code";
        results_id = "source_airport_results";
        url = "/search-airport?country="+country+"&state="+state+"&city="+city+"&airport=";
    }
    else if(k == 7){
        if (document.getElementById("destination_city_name")) {
            city = document.getElementById("destination_city_name").value.toLowerCase();
        }
        input_id = "destination_airport_code";
        results_id = "destination_airport_results";
        url = "/search-airport?country="+country+"&state="+state+"&city="+city+"&airport=";
    }


    return {input_id, results_id, url, city, state, country};
}

function search(k) {
    let {input_id, results_id, url} = resolve_variables(k);
    let input = document.getElementById(input_id);
    let filter = input.value.toLowerCase();
    let results = document.getElementById(results_id);

    // Clear previous results
    removeOptions(results_id);

    // Call API to get matching results
    fetch(url + filter)
    .then(response => response.json())
    .then(data => {
        if(data.data.length == 0){
            results.options[0].text = "No results found";
        }
        else{
            results.options[0].text = "Select a "+input_id.split("_")[0];
        }
        for (let i = 0; i < data.data.length; i++) {
            let result = data.data[i];
            let option = document.createElement("option");
            option.text = result;
            results.add(option);
        }

        // Show results select
        results.style.display = "block";
        let size = Math.max(1,Math.min(10, data.data.length+2));
        results.setAttribute("size", size);
    });
    //results.style.display = "block";
}

function hideResults(k) {
    let {results_id} = resolve_variables(k);
    let results = document.getElementById(results_id);
}

function selectResult(k) {
    let {input_id, results_id} = resolve_variables(k);
    let size = 0;
    let results = document.getElementById(results_id);
    results.setAttribute("size", size);
    let selectedOption = results.options[results.selectedIndex];
    let selectedValue = selectedOption.value;
    document.getElementById(input_id).value = selectedValue.split(',')[0];
}

function createFormElement(type, name, value) {
    let element = document.createElement("input");
    element.type = type;
    element.name = name;
    element.value = value;
    return element;
}
