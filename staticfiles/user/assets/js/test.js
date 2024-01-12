$(document).ready(function () {

    $('.payWith').click(function (e) {
        e.preventDefault();
        var fullname = $("[name='fullname']").val();
        var phoneno = $("[name='phoneno']").val();
        var house_no = $("[name='house_no']").val();
        var street = $("[name='street']").val();
        var district = $("[name='district']").val();
        var country = $("[name='country']").val();
        var state = $("[name='state']").val(); // Add the state variable
        var postcode = $("[name='postcode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();
        if (fullname == "" || phoneno == "" || postcode == "" || house_no == "" || street == "" || district == "" || state == "" || country == "") {
            Swal.fire("Alert!", "All fields are mandatory", "error");
            return false;
        } else {
            // Your AJAX code here...
            $.ajax({
                method: "GET",
                url: "/proceedtopay",
               
                success: function (response) {
                   console.log(response)
                }
                
            
                    });
                }
            });
        });
        