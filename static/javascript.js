// For username check availablility
var typingTimer;
var doneTypingInterval = 500;
$('#newid').on('keyup', function() {

    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
    document.getElementById("checkusername").innerHTML = "Checking...";

});
$('#newid').on('keydown', function() {
    clearTimeout(typingTimer);
});
function doneTyping(){

    // Only execute this function if 1 second is elapsed after typing.
    var data = document.getElementById('newid').value;
    // This sends the data first, and thereafter the synchronous flow is completed.
    $.ajax({
            url: "/check",
            type: "get",
            async: true,
            data: {username:data},
            // This function will happen after the synchronous flow
            success: function(data, status, header){
                 // console.log(data);
                 if(data === true){
                   document.getElementById("checkusername").style.color = "green";
                   document.getElementById("checkusername").innerHTML = "Username is available";
                   return true;
                 }
                 else{
                   document.getElementById("checkusername").style.color = "red";
                   document.getElementById("checkusername").innerHTML = "Username is unavailable. Choose another one";

                   // alert("Name is not available, choose another one!");
                   return false;
                 }
            },
            error: function(e){
                console.log(e);
                alert("ajax function does not run")
                return false;
            }
    });
    return false;
}
$('#backtoshop, #gotopay').on('click', function(e){

    console.log(e.target.id);
    if (e.target.id == 'backtoshop'){
        window.location.href ="/browse";
      } else {
        window.location.href = "/payment";
      }
});
$('#orderform').on('submit', function(e) {
  // e.preventDefault();
  var formdata = $('#orderform').serializeArray();
  // console.log(formdata);
  var logged = document.getElementById("not_hidden_prodid");
  console.log(logged);
  // if logged is true, means user not logged in. Direct to login page. Else preventDefault.
  if (!!logged === true){
    alert("Please log in to access that page. ");
    return true
  } else {
    e.preventDefault();

    // This sends the data first, and thereafter the synchronous flow is completed.
    $.ajax({
            url: "/add",
            type: "POST",
            async: true,
            data: formdata,
            // This function will happen after the synchronous flow
            success: function(data, status, header){
                 // console.log(data);
                 if(data == true){
                     $("#productmodal").click();
                     console.log("ajax add to cart sucess");
                     // alert("Item added to cart!");
                     return true;
                 }
                 else{
                     alert(data);
                     alert(status);
                     alert(header);
                     alert("Item cannot be added to cart. Please contact the system administrator.");
                     return false;
                 }
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log("Error: " + jqXHR.status);
                alert("ajax function does not run. Please contact the system administrator.");
            }
    });
  }
  // e.preventDefault();
  // return true;
});
$('#password, #confirmpassword').on('keyup', function () {

  var password = $('#password').val();
  if (/[a-zA-Z]+/.test(password) && /[0-9]+/.test(password)){
    $('#passwordhelp1').css('color', 'green');
  } else {
    $('#passwordhelp1').css('color', 'red');
  }

  if (password.length > 8) {
    $('#passwordhelp2').css('color', 'green');
  } else {
    $('#passwordhelp2').css('color', 'red');
  }

  if ($('#password').val() === $('#confirmpassword').val()) {
    $('#password').css('border-color', 'green');
    $('#confirmpassword').css('border-color', 'green');
  } else {
    $('#password').css('border-color', 'red');
    $('#confirmpassword').css('border-color', 'red');
  }
});

var all = document.getElementsByTagName("img");
var texts = document.getElementsByClassName("text-block");
var url = document.URL
var arr = [];
// We should only do things when the DOM is ready... because the js loads everything first, then check when document is ready.
$(document).ready(function() {
  if (url.substr(-1) === "/"){
    let docready = true;
    arr = Array.from(all);
    textarr = Array.from(texts);
    $("img[name = 'noshow']").css({"opacity": 0})

    // remove banner icon image from array.
    arr.shift();
    let timerId = setInterval(function(){

        // Remove gallery image
        let image = arr.shift();
        let text = textarr.shift();
        image.setAttribute("name", "noshow");
        text.setAttribute("name", "textnoshow");

        // append element to array.
        arr.push(image);
        textarr.push(text);

        // Change 1st array element to gallery image.
        arr[0].setAttribute("name", "stageimg");
        textarr[0].setAttribute("name", "textshow");
        $("img[name = 'stageimg']").fadeTo(250, 1);
        $("img[name = 'noshow']").css({"opacity": 0.5})
    }, 10000);
  }
  // Check page url. If product, do the following stuff.
  var lastpart = url.split("/")[3];
  if (lastpart === "product"){
    var modalbutton = document.getElementById("productmodal");
    modalbutton.style.visibility = "hidden";
    calculateprice();
    var line = document.getElementById("prodname").firstChild.data;
    var h = document.createElement("H1");
    names = ["Home", "", "Product"]
    link = ["/","","/browse","",line]
    var sign = "  >  ";

    for(var i = 0; i < 4; i++){
      if(i === 0 || i === 2) {
        var tags = document.createElement('a');
        tags.setAttribute('href', link[i]);
        tags.setAttribute('id', names[i].concat(i));
        tags.innerText = names[i];
        h.appendChild(tags);
      } else {
        h.appendChild(document.createTextNode(sign));
      }
    }
    h.appendChild(document.createTextNode(line));
    document.getElementById("top_product_liner").appendChild(h);
  }
  $('.minus').click(function () {
        var $input = $(this).parent().find('input');
				var count = parseInt($input.val()) - 1;
				count = count < 1 ? 1 : count;
				$input.val(count);
				$input.change();
        calculateprice();
				return false;
	});
	$('.plus').click(function () {
		var $input = $(this).parent().find('input');
		$input.val(parseInt($input.val()) + 1);
		$input.change();
    calculateprice();
		return false;
	});
  var delivercost = (5).toFixed(2);
  $("input[name = deliver_collect]").click(function(){
    if(document.getElementById("deliveryselect").checked){
       document.getElementById("delicost").innerHTML = "$" + delivercost.toString();
    } else {
      document.getElementById("delicost").innerHTML = "$0.00";
    }
    calculateprice();
  });
  $("#prod_img1, #prod_img2").click(function(event){
    // console.log("here");
    var tar = event.target;
    // console.log(tar);
    var source = tar.getAttribute("src");
    var id = tar.getAttribute("id");

    var main = document.getElementById("prod_img_main");
    var targetsrc = main.getAttribute("src");

    tar.setAttribute("src", targetsrc);
    main.setAttribute("src", source);
    return true;
  });

  if (lastpart === "cart"){

    var qty = 0;
    var subqty = 0;
    var price = parseFloat(0);
    var unitprice = 0;
    var totalprice = 0;
    var quantities = document.getElementById("cart-table");
    if (quantities != null){
      for (var i = 1; i < quantities.rows.length-1; i++){
        subqty = parseInt(quantities.rows[i].cells[2].innerHTML);
        qty += subqty;
        unitprice = parseFloat(quantities.rows[i].cells[3].innerHTML);
        price += unitprice;
        quantities.rows[i].cells[3].innerHTML = "$" + unitprice.toFixed(2);
        if (quantities.rows[i].cells[1].innerHTML === "Deliver"){
          var deliprice = parseFloat(5);
        } else {
          var deliprice = parseFloat(0);
        }
        subtotalprice = (subqty*unitprice) + deliprice;
        quantities.rows[i].cells[4].innerHTML = "$" + subtotalprice.toFixed(2);

        totalprice += subtotalprice;
      }
      document.getElementById("cart_totalqty").innerHTML = qty;
      document.getElementById("cart_totalprice").innerHTML = "$" + totalprice.toFixed(2);
    }

  }

  if (lastpart === "history"){

    var totprice = 0;
    var quantities = 0;
    var histtotalprice = document.getElementsByClassName("histtotalprice");
    var histunitprice = document.getElementsByClassName("histunitprice");
    // console.log(histothercols);
    // unit price and total paid are always on the 2nd 3rd index.
    for (var i = 0; i < histtotalprice.length; i++){
      var prod = parseFloat(histtotalprice[i].innerText);
      histtotalprice[i].innerHTML = "$" + prod.toFixed(2);
      // console.log(prod);
      var unit = parseFloat(histunitprice[i].innerText);
      histunitprice[i].innerHTML = "$" + unit.toFixed(2);
      // console.log(unit);
      totprice += prod;
      quantities += 1;
      document.getElementById("hist_totalqty").innerHTML = quantities;
      document.getElementById("hist_totalprice").innerHTML = "$" + totprice.toFixed(2);
    }
  }


  if (lastpart === "payment"){
    var deliverynum = document.getElementsByClassName("deliver");
    var totalprods = document.getElementsByClassName("prodprices");
    // console.log(totalprods);
    var count = 0;
    var prodprices = 0;
    for (var i = 0; i < deliverynum.length; i++){
      if (deliverynum[i].innerText === "Deliver"){
          count = count + 1;
      }
      var prod = parseFloat(totalprods[i].innerText);
      // console.log(prod);
      targetid = "prodprice" + i.toString();
      document.getElementById(targetid).innerHTML = "$" + prod.toFixed(2);
      prodprices += parseFloat(prod);
    }
    // console.log(prodprices);
    var totaldeliverycost = count * 5.00;
    document.getElementById("totaldeliverycost").innerHTML = "$" + totaldeliverycost.toFixed(2);
    finaltotal = prodprices + totaldeliverycost;
    document.getElementById("finaltotal").innerHTML = "$" + finaltotal.toFixed(2);
  }
  $('.paymentremove').click(function(e){

    var index = "removeproductpayment" + e.toElement.id;
    console.log(index);
    var payform = document.getElementById(index);
    // document.forms[index].submit();
    // console.log(payform);
    if (payform === null){
      var keyword = "hiddenremovepay" + e.toElement.id;
      var input = document.getElementById(keyword);
      var newform = document.createElement("FORM");
      newform.action = "/removeproduct";
      newform.method = "post";
      newform.appendChild(input);
      // console.log(payform);
      document.body.appendChild(newform);
      newform.submit();
    } else{
      payform.submit();
    }
  });
});

function paylah(){
  $(".ccdetails").hide();
  $(".ccdetails").required = false;
  $(".paylah").show();
  return true;
}
function ccard(){
  $(".ccdetails").required = true;
  $(".ccdetails").show();
  return true;
}
function removeproductcart(e){

  var row = e.id; // id 1 is row 2, id 2 is row 3.
  var rowindex = e.parentNode.childNodes[1];
  rowindex.submit();
  // console.log(row);
  // console.log(rowindex);
  // https://gomakethings.com/how-to-get-all-of-an-elements-siblings-with-vanilla-js/
  // console.log($("input[name = remove_prodid]"));

}
function calculateprice(){
  var deliver = parseInt(document.getElementById("delicost").innerHTML.slice(1));
  var qty = parseInt(document.getElementById("order_quantity").value);
  var price = parseFloat(document.getElementById("pricevar").innerHTML.slice(1));
  var subtotal = (qty*price).toFixed(2);
  var final = qty*price + deliver;
  var finalfloat = final.toFixed(2);
  // console.log(finalfloat);
  document.getElementById("quantityvar").innerHTML = qty;
  document.getElementById("totcost").innerHTML = "$" + finalfloat.toString();
  document.getElementById("subcost").innerHTML = "$" + subtotal.toString();
  return true;
}

if (window.matchMedia("(max-width: 768px)").matches){

  console.log("max width is 768");
} else {
  console.log("Max width is not 768px");
}
