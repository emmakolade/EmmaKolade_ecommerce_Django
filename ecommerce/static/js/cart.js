var updateCart = document.getElementsByClassName("update-cart");

for (i = 0; i < updateCart.length; i++) {
  updateCart[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log("productId:", productId, "action:", action);

    console.log("USER:", user);
    if (user == "AnonymousUser") {
      addCookieItem(productId, action)
    } else {
      updateUserOrder(productId, action);
    }
  });
}

// add cookie when the user is not loggedin
function addCookieItem(productId, action){
  console.log("not logged in");
  // increase and decrease the value ofthe cart
  if(action == 'add'){
    if(cart[productId] == undefined){
      cart[productId] = {'quantity': 1}
    }
    else{
      cart[productId]['quantity'] += 1
    }
  }

  if(action == 'remove'){
    cart[productId]['quantity'] -= 1
    if(cart[productId]['quantity']){
      console.log('remove item')
      delete cart[productId]

    }
  }
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/" //overrides whatever the cookie has set for the path
  location.reload() // rest api is better here
}


// to update user order

function updateUserOrder(productId, action) {
  console.log("user logged in");
  var url = "/added_item/";
  // to send POST data
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    // return response as a promise to fetch
    .then((response) => {
      return response.json();
    })

    .then((data) => {
      console.log("date:", data);
      location.reload();
    });
}



