/* jshint eversion: 6 */

'use strict';

class Item {
    constructor(name, quantity, price, store, section, priority) {
        this.name = name;
        this.quantity = quantity;
        this.price = price;
        this.store = store;
        this.section = section;
        this.priority = priority;

        this._purchased = false;
    }

    get purchased() {
        return this._purchased;
    }

    set purchased(newValue) {
        this._purchased = newValue;
    }
}

class Subject {
    constructor() {
        this.handlers = []
    }

    subscribe(fn) {
        this.handlers.push(fn);
    }

    unsubscribe(fn) {
        this.handlers = this.handlers.filter(
            function(item) {
                if (item !== fn) {
                    return item;
                }
            }
        );
    }

    publish(msg, someobj) {
        var scope = someobj || window;
        for (let fn of this.handlers) {
            fn(scope, msg)
        }
    }
}


class ShoppingList extends Subject {
    constructor() {
        super();
        this.items = [];
    }

    loadFromStorage() {
        this.items = localStorage.getItem("shoppinglist") ? JSON.parse(localStorage.getItem("shoppinglist")) : [];
        this.publish('update', this);
    }

    saveToStorage() {
        localStorage.setItem("shoppinglist", JSON.stringify(this.items));
    }
    
    addItem(item) {
        this.items.push(item);
        this.publish('update', this);
    }
    
    cleanList() {
        this.items.splice(0);
        this.publish('update', this);
    }

    cleanPurchased() {
        this.items = this.items.filter(function(item) { 
            return item.purchased === true;
        });
        this.publish('update', this);
    }
    
    emptyList() {
        this.items = [];
        this.publish('update', this);
    }
}