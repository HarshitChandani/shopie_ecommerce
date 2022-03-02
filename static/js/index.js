   $(window).on("load",()=>{
      get_cart();
   });

   $(document).ready(function() {

      var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

      $(".add_to_cart_btn").on('click',function(){
         user_selected_product_size = $("input[name='radio-sizes']:checked").val();
         product_slug = this.id;
         default_qty = parseInt(1)
         if (!user_selected_product_size){
            alert("Please select size.")
         }
         else{
            $.ajax({
               url: "http://127.0.0.1:8000/add-to-cart/",
               method:"POST",
               data: {
                  product_slug:product_slug,
                  user_selected_size:user_selected_product_size,
                  default_qty:default_qty
               },
               headers:{
                  'X-CSRFToken':csrfToken
               },
               success:(data) => {
                  if (data){
                     console.log("Item added to cart.")
                     location.reload(true);
                     alert("Item added to cart. ")
                     // $("#cart-total-items").html(data)
                     // $("#item-add-success-alert")
                     //    .fadeTo(2000, 500)
                     //    .slideUp(500, function() {
                     //       $("#item-add-success-alert").slideUp(500);
                     //    })
                     //    .css("display","block")
                     //    .html("<strong><i class='fas fa-check'></i> Item added.</strong>");
                     //    $("#item-add-failure-alert").css("display","none")
                        get_cart()
                  }
                  else{
                     console.log("Item added to cart.")
                     $("#item-add-failure-alert")
                        .fadeTo(2000, 500)
                        .slideUp(500, function() {
                           $("#item-add-success-alert").slideUp(500);
                        })
                        .css("display","block")
                        .html("<strong><i class='fas fa-check'></i>Error .</strong>");
                     $("#item-add-success-alert").css("display","none")                       
                  }
               }
            });
         }
      })

      

      $("#see-password").on("click",function(){
         attribute_value = "text"
         if ($("#password").attr("type") == attribute_value) {
            $("#password").attr("type","password")
         }
         else{
            $("#password").attr("type","text")
         }
      })
      
   })

   // click click to add item to a wishlist
   function add_to_wishlist(id){
      $("#"+id).css("color","#f42d2a");
   }
   
  function get_cart(){
     $.ajax({
         url: "http://127.0.0.1:8000/add-to-cart/",
         method:"GET",
         success:(data)=>{
            console.log(data)
            $("#cart-total-items").html(data)
         }
       });
   }
   function increment_qty(product_slug){
      current_qty = parseInt($("#"+product_slug+"_qty").val())
      $.ajax({
         url:"/increase_qty/",
         method:"GET",
         data:{
            id:product_slug,
         },
         success:(data)=>{
            if (data.cart_updated){
               $("#cart-net-amt").html("₹ "+data.cart_total);
               $("#cart-gross-amt").html("₹ "+data.cart_total);
               $("#"+product_slug+"_qty").val(current_qty+1);
               console.log(data);
            }else{
               console.log(data.reason);
            }
         }
      })
   }
   function decrement_qty(product_slug){
      current_qty = parseInt($("#"+product_slug+"_qty").val())
      $.ajax({
         url:"/decrease_qty/",
         method:"GET",
         data:{
            id:product_slug,
         },
         success:(data)=>{
            if (data.cart_updated){
               $("#cart-net-amt").html("₹ "+data.cart_total);
               $("#cart-gross-amt").html("₹ "+data.cart_total);
               $("#"+product_slug+"_qty").val(current_qty-1);
               console.log(data);
            }else{
               console.log(data.reason);
            }
         }
      })
   }
  
   function create_order(){
      address_selected = $("input[name='address-radio']:checked").val()
      csrfToken = $("input[name=csrfmiddlewaretoken]").val();
      $(".create-order-loading").css("visibility","visible");
      $("#checkout_btn").attr("disabled", true);
      $.ajax({
         url : '/checkout/',
         method:"POST",
         data:{
            address_id: address_selected
         },
         headers: {
            'X-CSRFToken':csrfToken
         },
         success: (data)=>{
            if (data.order_placed){
               $(".create-order-loading").css("visibility","hidden");
               alert("Your order has been placed.")
               window.location.href = 'http://127.0.0.1:8000/'
            }
            else{
               console.log("Invalid.")
               alert("Invalid")
            }
         }
      })
   }