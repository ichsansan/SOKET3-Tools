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

function getTagLists(unit) {
    console.log('Getting tag lists from ', unit);
    $.ajax({
        type: "get",
        url: "/services/historian-recap/taglists/" + unit,
        success: function (response) {
            // var Element = document.getElementById('reportsChart');
            console.log(response);
            if (response.status == 'success') {
                var content = response.content;
                content.forEach(line => {
                    line["Add"] = `<button class="btn btn-light btn-sm rounded-5" onclick="addTags('${line['TagName']}')"><i class="fas fa-plus"/></button>`
                });
                dict_to_table(content, 'tagLists');

            }
            else {
                console.log('Failed');
            }
        }
    });
};

function getTagRecap(unit) {
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
};

function plotTag(unit) {
    var tagname = document.getElementById('tagName').value;
    var realtimeData = document.getElementById('realtimeData');
    var realtimeDataHTML = document.getElementById('realtimeDataHTML');

    realtimeData.innerHTML = `<div class="text-center"><i class="fas fa-3x fa-spinner fa-spin-pulse"></i></div>`;
    console.log(`Getting tag ${tagname} from unit ${unit}`);

    $.ajax({
        type: "get",
        url: `/services/historian-recap/plot/${unit}/${tagname}`,
        success: function (response) {
            console.log(response);
            realtimeDataHTML.innerHTML = response['content'][''];
            // realtimeData.innerHTML = `<iframe src="/${response['content']['figure_loc']}" style="min-height: 400px; width: 100%;></iframe>`;
        }
    });
}

function addTags(tag) {
    var Window = document.getElementById('tagsWindow');
    var tagSelected = [];
    console.log(tag);

    $.each($('#tagsWindow').children(), function (i, el) {
        tagSelected.push(el.id);
    });
    if (!(tagSelected.includes(`tag-${tag}`))) {
        Window.innerHTML += `<button type="button" class="btn btn-sm btn-light rounded-5 tags-item" id="tag-${tag}" tagname="${tag}" onclick="delTags(this)">${tag}</button>`
        $(`[onclick*=addTags][onclick*=${tag}]`).each(function (i, element) {
            if (!$(element).hasClass('selected')) {
                $(element).addClass('selected');
            }
        });
    }
}
function delTags(element) {
    console.log('Deleting', element.getAttribute('tagname'));
    var id = String(element.getAttribute('tagname'));
    element.remove();
    console.log('Deleting', id);

    $(`[onclick*=addTags][onclick*=${id}]`).each(function (i, e) {
        $(e).removeClass('selected');
    });
}

function validateTags(mode = 'plot') {
    var tagSelected = [];
    $.each($('#tagsWindow').children(), function (i, el) {
        tagSelected.push(el.id.replace('tag-', ''));
    });
    if ((tagSelected.length > 10) & (mode == 'plot')) {
        alert('Cuma bisa ngeplot 10 tag. Coba dikurangi lagi.');
    } else if (tagSelected.length == 0) {
        alert('Pilih tag untuk diplot');
    } else {
        var redirectUrl = window.location.origin + window.location.pathname;
        var payload = {
            "tags": tagSelected.join(',')
        };
        var queryString = Object.keys(payload).map(function (key) {
            return key + '=' + payload[key];
        }).join('&');

        console.log(`Redirecting to: "${redirectUrl}?${queryString}"`);
        window.location = `${redirectUrl}?${queryString}`;
    }
}
