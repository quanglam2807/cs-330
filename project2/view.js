/* jshint eversion: 6 */

'use strict';


class ShoppingView {
    constructor(model) {
        model.subscribe(this.redrawList.bind(this));
    }

    redrawList(shoppingList, msg) {
        var tbl = document.querySelector("#tbody");
        tbl.innerHTML = "";
        for (var item of shoppingList.items) {
            this.addRow(item, tbl);
        }
    }
    
    addRow(item, tbl) {  
        var row = document.createElement("tr");

        switch (item.priority) {
            case 'high':
                row.className = 'table-danger';
                break;
            case 'medium':
                row.className = 'table-warning';
                break;
            default:
                row.className = 'table-success';
        }

        var cell0 = document.createElement("td");
        var checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = Boolean(item.purchased);
        checkbox.onclick = function() {
            item.purchased = checkbox.checked;
        };
        cell0.appendChild(checkbox);
        var cell1 = document.createElement("td");
        cell1.innerText = item.name;
        var cell2 = document.createElement("td");
        cell2.innerText = item.quantity;
        var cell3 = document.createElement("td");
        cell3.innerText = item.name;
        var cell4 = document.createElement("td");
        cell4.innerText = item.section;
        var cell5 = document.createElement("td");
        cell5.innerText = item.price;
        
        row.appendChild(cell0);
        row.appendChild(cell1);
        row.appendChild(cell2);
        row.appendChild(cell3);
        row.appendChild(cell4);
        row.appendChild(cell5);
        tbl.appendChild(row);
    }
}