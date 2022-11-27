$(".toggle-sidebar-btn").click(function () {
    $("body").toggleClass("toggle-sidebar");
})

function dict_to_table(data, Element) {
    let col = data.columns;
    let content = data.content;
    console.log(col);

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
    if (content.length == 0) {
        tr = table.insertRow(-1);
        cell = tr.insertCell(-1);
        cell.setAttribute('colspan', col.length);
        cell.className = 'text-center';
        cell.innerHTML = "No updates";
    } else {
        for (let i = 0; i < content.length; i++) {
            tr = table.insertRow(-1);
            for (let j = 0; j < col.length; j++) {
                let tabCell = tr.insertCell(-1);
                tabCell.innerHTML = content[i][col[j]];
            }
        }
    }
    
    // Now, add the newly created table with json data, to a container.
    Element.innerHTML = "";
    Element.appendChild(table);
}

function refreshDaftarIsi(element_name, project_name, periods) {
    document.getElementById(element_name).innerHTML = "<div class=\"text-center h-100\" style=\"transform: translateY(40%);\"><i class=\"fas fa-3x fa-spinner fa-spin-pulse fa-spin-reverse\"></i></div>"
    $("#" + element_name).prev().children()[0].innerHTML = "/ " + periods;

    $.ajax({
        type: "get",
        url: "/services/daftar-isi/compare",
        data: {'project_name':project_name, 'daterange':periods},
        success: function (response) {
            var Element = document.getElementById(element_name);
            try {
                var content = response.content;
                
                dict_to_table(content, Element);
            } catch (error) {
                console.log(error);
            }
        }
    });
}

$(document).ready(function () {
    refreshDaftarIsi('PJBBoxReports','PJB Box SOKET3','Today');
    refreshDaftarIsi('tbOfContent', 'PJB Box SOKET3', '60 Day');
});

