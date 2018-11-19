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

class ShoppingList {
    constructor() {
        this.items = [];
    }


    addItem(item) {
        this._items.push(item);
    }

    cleanList() {
        this._items.splice(0);
    }

    emptyList() {
        this._items = [];
    }
}