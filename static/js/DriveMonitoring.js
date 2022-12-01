$(".toggle-sidebar-btn").click(function () {
    $("body").toggleClass("toggle-sidebar");
})

function dict_to_table(data, Element) {
    let col = data.columns;
    let content = data.content;
    let page = 0;
    let limit = 0;
    let total = 0;
    
    if ('page' in data.pagination){
        page = data.pagination.page;
    }
    if ('limit' in data.pagination){
        limit = data.pagination.limit;
    }
    if ('total' in data.pagination){
        total = data.pagination.total;
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

    // Create number of pages
    for (let i = 0; i < parseInt(total/limit); i++) {
        const element = parseInt(total/limit);
    }

    // Create pagination elements
    const nav = document.createElement('nav');
    let ul = document.createElement('ul');
    ul.className = "pagination justify-content-center";

    
    // Now, add the newly created table with json data, to a container.
    Element.innerHTML = "";
    Element.appendChild(table);
}

function refreshDaftarIsi(element_name, project_name, periods, nlimit, npage) {
    document.getElementById(element_name).innerHTML = "<div class=\"text-center h-100\" style=\"transform: translateY(40%);\"><i class=\"fas fa-3x fa-spinner fa-spin-pulse fa-spin-reverse\"></i></div>"
    $("#" + element_name).prev().children()[0].innerHTML = "/ " + periods;

    $.ajax({
        type: "get",
        url: "/services/daftar-isi/compare",
        data: {'project_name':project_name, 'daterange':periods, nlimit:nlimit, npage:npage},
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

function refreshRecentActivity(element_name, project_name) {
    document.getElementById(element_name).innerHTML = "<div class=\"text-center h-100\" style=\"transform: translateY(40%);\"><i class=\"fas fa-3x fa-spinner fa-spin-pulse fa-spin-reverse\"></i></div>"
    // $("#" + element_name).prev().children()[0].innerHTML = "/ " + periods;

    $.ajax({
        type: "get",
        url: "/service/daftar-isi/recent-activity",
        data: {'project_name':project_name},
        success: function (response) {
            var Element = document.getElementById(element_name);
            try {
                var content = response.content;
                
                htmlcontent = '';
                for (const i in content) {
                    var date = content[i]['date'];
                    var event = content[i]['event'];
                    var color = content[i]['color'];
                    
                    htmlcontent += `\
                        <div class="activity-item d-flex"> \
                            <div class="activite-label">${date}</div> \
                            <i class="fas fa-xs fa-circle me-2 activity-badge ${color} align-self-start"></i> \
                            <div class="activity-content"> ${event} </div> \
                        </div>`;
                }
                document.getElementById(element_name).innerHTML = htmlcontent;
            } catch (error) {
                console.log(error);
            }
        }
    });
}



