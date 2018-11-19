/* jshint eversion: 6 */

'use strict';

var stores = ['Fareway', 'Ace Hardware', 'Casey\'s', 'The Hatchery', 'Kwik Star', 'C-Store'];
var sections = ['Produce', 'Meats', 'Cereal', 'Canned Goods', 'Frozen Foods', 'Dairy', 'Liquor', 'Tools', 'Clothing'];

var shoppingList = new ShoppingList();
var appView = new ShoppingView(shoppingList);

function listToSelect(selectId, sList) {
    var sel = document.getElementById(selectId, sList);
    for (var s of sList) {
        var opt = document.createElement("option");
        opt.value = s;
        opt.innerHTML = s;
        sel.appendChild(opt);
    }
}

function addItem() {
    var name = document.querySelector("#name").value;
  
    var e1 = document.querySelector("#quantity");
    var quantity = e1.options[e1.selectedIndex].value;

    console.log(quantity);
  
    var e2 = document.querySelector("#priority");
    var priority = e2.options[e2.selectedIndex].value;
  
    var e3 = document.querySelector("#store");
    var store = e3.options[e3.selectedIndex].value;
  
    var e4 = document.querySelector("#section");
    var section = e4.options[e4.selectedIndex].value;
    
    var price = document.querySelector("#price").value;
  
    if (!name) {
      alert("Please enter item name.");
      return;
    }
  
    if (!price) {
      alert("Please enter price.");
      return;
    }

    var item = new Item(name, quantity, price, store, section, priority);
    shoppingList.addItem(item);
}

function saveList() {
    shoppingList.saveToStorage();
}

function clearList() {
    shoppingList.cleanList();
}

function clearPurchased() {
    shoppingList.cleanPurchased();
}
  
$(document).ready(function () {
    listToSelect('store', stores);
    listToSelect('section', sections);
    
    shoppingList.loadFromStorage();

    document.querySelector("#add_item").addEventListener("click", addItem);
    document.querySelector("#save_list").addEventListener("click", saveList);
    document.querySelector("#clear_list").addEventListener("click", clearList);
    document.querySelector("#clear_purchased").addEventListener("click", clearPurchased);
});