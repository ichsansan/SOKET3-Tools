function dict_to_table(content, ElementID) {
    let Element = document.getElementById(ElementID);
    let col = [];
    for (let i = 0; i < content.length; i++) {
        for (let key in content[i]) {
            if (col.indexOf(key) === -1) {
                col.push(key);
            }
        }
    }

    // Create table.
    const table = document.createElement("table");
    table.className = 'table table-hover table-sm table-borderless';

    // Create table header row using the extracted headers above.
    let tr = table.insertRow(-1);                   // table row.

    for (let i = 0; i < col.length; i++) {
        let th = document.createElement("th");      // table header.
        th.innerHTML = col[i];
        tr.appendChild(th);
    }

    // add json data to the table as rows.
    for (let i = 0; i < content.length; i++) {

        tr = table.insertRow(-1);

        for (let j = 0; j < col.length; j++) {
            let tabCell = tr.insertCell(-1);
            tabCell.innerHTML = content[i][col[j]];
        }
    }

    // Now, add the newly created table with json data, to a container.
    Element.innerHTML = "";
    Element.appendChild(table);
}

function getTagLists(unit){
    console.log('Getting tag lists from ', unit);
    $.ajax({
        type: "get",
        url: "/services/historian-recap/" + unit,
        success: function (response) {
            // var Element = document.getElementById('reportsChart');
            console.log(response);
            if (response.status == 'success') {
                var content = response.content;
                
                dict_to_table(content, 'tagLists');
            }
            else {
                console.log('Failed');
            }
        }
    });
};

function getTagRecap(unit){
    console.log('Getting tag recap from ', unit);
    $.ajax({
        type: "get",
        url: "/services/historian-tag-recap/" + unit,
        success: function (response) {
            // var Element = document.getElementById('reportsChart');
            console.log(response);
            if (response.status == 'success') {
                var content = response.content;
                
                document.getElementById('tagcount').innerHTML = content['tagcount'];
                document.getElementById('startdate').innerHTML = content['startdate'];
                document.getElementById('enddate').innerHTML = content['enddate'];
            }
            else {
                console.log('Failed');
            }
        }
    });

    console.log('Getting daily availability from ', unit);
    $.ajax({
        type: "get",
        url: "/services/historian-daily-availability/" + unit,
        success: function (response) {
            console.log(response);
            if (response.status == 'success') {
                let content = response.content;
                let table = document.createElement('table');
                table.className = 'table table-hover table-sm table-borderless';

                for (const key in content) {
                    let tr = table.insertRow(-1);
                    let th = document.createElement('th');
                    th.innerHTML = key;
                    tr.appendChild(th);
                    
                    let td = document.createElement('td');
                    td.innerHTML = parseFloat(content[key]).toPrecision(2) + " %";
                    tr.appendChild(td);
                }
                document.getElementById('dailyAvailability').innerHTML = "";
                document.getElementById('dailyAvailability').appendChild(table);
            }
            else {
                console.log('Failed');
            }
        }
    });
};
