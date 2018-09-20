/* jshint esversion: 6 */
"use strict";

function addItem(n) {
  var itemName = document.querySelector("#itemName").value;

  var e1 = document.querySelector("#quantity");
  var quantity = e1.options[e1.selectedIndex].value;

  var e2 = document.querySelector("#priority");
  var quantity = e2.options[e2.selectedIndex].value;

  var e3 = document.querySelector("#storeName");
  var storeName = e3.options[e3.selectedIndex].value;

  var e4 = document.querySelector("#storeSection");
  var storeSection = e4.options[e4.selectedIndex].value;
  
  var price = document.querySelector("#price").value;

  if (!itemName) {
    alert("Please enter item name.");
    return;
  }

  if (!price) {
    alert("Please enter price.");
    return;
  }

  var tbody = document.querySelector("#tbody");

  var row = document.createElement("tr");
  var cell0 = document.createElement("td");
  var checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  cell0.appendChild(checkbox);
  var cell1 = document.createElement("td");
  cell1.innerText = itemName;
  var cell2 = document.createElement("td");
  cell2.innerText = quantity;
  var cell3 = document.createElement("td");
  cell3.innerText = storeName;
  var cell4 = document.createElement("td");
  cell4.innerText = storeSection;
  var cell5 = document.createElement("td");
  cell5.innerText = price;
  row.appendChild(cell0);
  row.appendChild(cell1);
  row.appendChild(cell2);
  row.appendChild(cell3);
  row.appendChild(cell4);
  row.appendChild(cell5);
  tbody.appendChild(row);
}

document.querySelector("#add_item").addEventListener("click", addItem);