/* jshint eversion: 6 */

'use strict';

class Item {
    constructor(name, quantity, price, store, section, priority) {
        this._name = name;
        this._quantiy = quantity;
        this._price = price;
        this._store = store;
        this._section = section;
        this._priority = priority;

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
        this._items = [];
    }
}

ShoppingList.prototype.addItem = function(item) {
    this._items.push(item);
};

ShoppingList.prototype.cleanList = function() {
    this._items.splice(0);
};

ShoppingList.prototype.emptyItem = function() {
    this._items = [];
};