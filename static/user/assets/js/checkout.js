






//  $(document).ready(function () {

//     $('.payWithRazorpay').click(function (e) {
//         e.preventDefault();
        
//         // var fullname = $("[name='fullname']").val();
//         // var phoneno = $("[name='phoneno']").val();
//         // var house_no = $("[name='house_no']").val();
//         // var street = $("[name='street']").val();
//         // var district = $("[name='district']").val();
//         // var country = $("[name='country']").val();
//         // var state = $("[name='state']").val(); // Add the state variable
//         // var postcode = $("[name='postcode']").val();
//         var token = $("[name='csrfmiddlewaretoken']").val();
//         // if (fullname == "" || phoneno == "" || postcode == "" || house_no == "" || street == "" || district == "" || state == "" || country == "") {
//         //     Swal.fire("Alert!", "All fields are mandatory", "error");
//         //     return false;
//         // } else 
        
//             // Your AJAX code here...
//             $.ajax({
//                 method: "GET",
//                 url: "ur",
//                 success: function (response) {
//                     console.log(response.total1); // Correctly log the 'total1' value from the response
//                     // You can now use the 'total1' value as needed for further processing
//                     // For example, update the payment amount in your UI
//                 },
//                 error: function (xhr, status, error) {
//                     // Handle the error if the AJAX request fails
//                     console.error(error);
//                 }
//             });
//             // var options = {
//             //     "key": "YOUR_KEY_ID", // Enter the Key ID generated from the Dashboard
//             //     "amount": "50000", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
//             //     "currency": "INR",
//             //     "name": "Acme Corp", //your business name
//             //     "description": "Test Transaction",
//             //     "image": "https://example.com/your_logo",
//             //     "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
//             //     "handler": function (response){
//             //         alert(response.razorpay_payment_id);
//             //         alert(response.razorpay_order_id);
//             //         alert(response.razorpay_signature)
//             //     },
//             //     "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
//             //         "name": "Gaurav Kumar", //your customer's name
//             //         "email": "gaurav.kumar@example.com", 
//             //         "contact": "9000090000"  //Provide the customer's phone number for better conversion rates 
//             //     },
//             //     "notes": {
//             //         "address": "Razorpay Corporate Office"
//             //     },
//             //     "theme": {
//             //         "color": "#3399cc"
//             //     }
//             // };
//             // var rzp1 = new Razorpay(options);
//             // rzp1.open();
//             // // Razorpay payment gateway initialization code here...
        
//     });
// });


