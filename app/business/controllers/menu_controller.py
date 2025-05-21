from app import db
from app.business.models.menu import Menu
from flask import jsonify
from app.business.models.product import Product
from app.business.models.restaurant import Restaurant
from flask import request


class MenuController:
    @staticmethod
    def get_all():
        menus = Menu.query.all()
        return [menu.to_dict() for menu in menus]
    
    @staticmethod
    def get_by_id(menu_id):
        menu = Menu.query.get_or_404(menu_id)
        return menu.to_dict()
    
    @staticmethod
    def create(data):
        new_menu = Menu(
            restaurant_id=data.get('restaurant_id'),
            product_id=data.get('product_id'),
            price=data.get('price'),
            availability=data.get('availability', True)
        )
        
        db.session.add(new_menu)
        db.session.commit()
        
        return new_menu.to_dict(), 201
    
    @staticmethod
    def update(menu_id, data):
        menu = Menu.query.get_or_404(menu_id)
        
        if 'restaurant_id' in data:
            menu.restaurant_id = data['restaurant_id']
        if 'product_id' in data:
            menu.product_id = data['product_id']
        if 'price' in data:
            menu.price = data['price']
        if 'availability' in data:
            menu.availability = data['availability']
        
        db.session.commit()
        
        return menu.to_dict()
    
    @staticmethod
    def delete(menu_id):
        menu = Menu.query.get_or_404(menu_id)
        
        db.session.delete(menu)
        db.session.commit()
        
        return {"message": "Menu item deleted successfully"}, 200

    @staticmethod
    def get_by_restaurant_id(restaurant_id):
        menus = Menu.query.filter_by(restaurant_id=restaurant_id).all()
        return [menu.to_dict() for menu in menus]

    @staticmethod
    def search_by_product_name():
        name = request.args.get('name')
        if not name:
            return jsonify({"error": "Missing 'name' parameter"}), 400

        menus = Menu.query.join(Menu.product).join(Menu.restaurant) \
            .filter(Product.name.ilike(f"%{name}%")).all()

        result = []
        for menu in menus:
            result.append({
                'menu_id': menu.id,
                'product_name': menu.product.name,
                'restaurant_name': menu.restaurant.name
            })

        return jsonify(result)