$(document).ready(function() {
    var page = 1;
    var items_per_page = 2; 

    function fetchData() {
        $.ajax({
            url: "fetchUsers.php",
            type: "GET",
            data: { page: page },
            dataType: 'json',
            success: function(response) {
                var data = response.data;
                var total = parseInt(response.total);
                var table = $("#data-table");
                
                table.find("tr:gt(0)").remove();
   
                data.forEach(function(user) {
                    var row = `<tr>
                        <td>${user.nume}</td>
                        <td>${user.prenume}</td>
                        <td>${user.telefon}</td>
                        <td>${user.email}</td>
                    </tr>`;
                    table.append(row);
                });

                $("#prev-btn").prop("disabled", page === 1);
                $("#next-btn").prop("disabled", page * items_per_page >= total);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("Eroare:", textStatus, errorThrown);
            }
        });
    }

    $("#prev-btn").click(function() {
        if (page > 1) page--;
        fetchData();
    });

    $("#next-btn").click(function() {
        page++;
        fetchData();
    });

    fetchData(); 
});