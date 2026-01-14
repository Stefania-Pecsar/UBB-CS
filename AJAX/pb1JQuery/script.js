function getPlecari() {
    var url = "plecari.php";
    $.get(url, function(data) {
        $('#orasPlecare').html(data);
    });
}

function getSosiri(value) {
    console.log("Trimis către server:", value);
    $.get("sosiri.php", { name: value }, function(data) {
        console.log("Răspuns primit:", data); 
        $('#orasSosire').html(data);
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.error("Eroare AJAX:", textStatus, errorThrown); 
        $('#orasSosire').html('<option>Eroare la incarcare</option>');
    });
}