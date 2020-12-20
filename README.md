# inventorymgr #

Inventory management system for use in small organizations, written
using Flask, Vue.js and Bulma.

## Features ##

* Create, manage and invite users.
* Create and manage borrowable items.
* Users and items can be associated with qualifications
  (think: driver's license or similar). 
* Checkout items to a user.
* Check-in borrowed items.

## Roadmap ##

* Generate barcodes compatible with EAN-13 scanners for user IDs and item IDs.

## Dependencies ##

Server-side:

* [Flask](https://palletsprojects.com/p/flask/)
* [Flask-SQLAlchemy](https://github.com/pallets/flask-sqlalchemy)
* [pydantic](https://github.com/samuelcolvin/pydantic/)

Client-side (bundled with inventorymgr):

* [Vue.js](https://github.com/vuejs/vue)
* [vue-router](https://github.com/vuejs/vue-router)
* [vuex](https://github.com/vuejs/vuex)
* [vue-i18n](https://github.com/kazupon/vue-i18n)
* [Bulma](https://github.com/jgthms/bulma)

Development:

* [mypy](http://www.mypy-lang.org/)
* [pylint](https://github.com/PyCQA/pylint)
* [pytest](https://docs.pytest.org/en/latest/)
* [black](https:/github.com/psf/black)

## License ##

inventorymgr is licensed under the MIT license, see LICENSE for details.
