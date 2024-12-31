from flask import request, jsonify
from flask_restx import Api, Resource, fields
from app import create_app
from app.repository import WalletRepository

app = create_app()
api = Api(app, title="Wallet API", description="API para gerenciar carteiras digitais", doc="/swagger/")

repo = WalletRepository()

# Modelos para o Swagger
wallet_model = api.model('Wallet', {
    'id': fields.Integer(readOnly=True, description='ID da carteira'),
    'name': fields.String(required=True, description='Nome da carteira'),
    'balance': fields.Float(readOnly=True, description='Saldo da carteira')
})

create_wallet_model = api.model('CreateWallet', {
    'name': fields.String(required=True, description='Nome da carteira')
})

transaction_model = api.model('Transaction', {
    'amount': fields.Float(required=True, description='Valor da transação')
})

transfer_model = api.model('Transfer', {
    'from_wallet_id': fields.Integer(required=True, description='ID da carteira de origem'),
    'to_wallet_id': fields.Integer(required=True, description='ID da carteira de destino'),
    'amount': fields.Float(required=True, description='Valor a ser transferido')
})


@api.route('/wallets')
class WalletList(Resource):
    @api.expect(create_wallet_model)
    @api.marshal_with(wallet_model, code=201)
    def post(self):
        """Cria uma nova carteira"""
        data = request.json
        wallet = repo.create_wallet(data["name"])
        return wallet, 201


@api.route('/wallets/<int:wallet_id>')
class Wallet(Resource):
    @api.marshal_with(wallet_model)
    def get(self, wallet_id):
        """Consulta uma carteira pelo ID"""
        wallet = repo.get_wallet(wallet_id)
        if wallet is None:
            api.abort(404, "Wallet not found")
        return wallet
    
    @api.expect(create_wallet_model)
    @api.marshal_with(wallet_model)
    def put(self, wallet_id):
        """Atualiza o nome de uma carteira"""
        data = request.json
        wallet = repo.update_wallet(wallet_id, data.get("name"))
        if wallet is None:
            api.abort(404, "Wallet not found")
        return wallet

    def delete(self, wallet_id):
        """Exclui uma carteira pelo ID"""
        wallet = repo.delete_wallet(wallet_id)
        if wallet is None:
            api.abort(404, "Wallet not found")
        return '', 204


@api.route('/wallets/<int:wallet_id>/deposit')
class Deposit(Resource):
    @api.expect(transaction_model)
    @api.marshal_with(wallet_model)
    def post(self, wallet_id):
        """Deposita um valor na carteira"""
        data = request.json
        wallet = repo.deposit(wallet_id, data["amount"])
        if wallet is None:
            api.abort(404, "Wallet not found")
        return wallet


@api.route('/wallets/<int:wallet_id>/withdraw')
class Withdraw(Resource):
    @api.expect(transaction_model)
    @api.marshal_with(wallet_model)
    def post(self, wallet_id):
        """Saca um valor da carteira"""
        data = request.json
        wallet = repo.withdraw(wallet_id, data["amount"])
        if wallet is None:
            api.abort(400, "Insufficient balance or wallet not found")
        return wallet


@api.route('/wallets/transfer')
class Transfer(Resource):
    @api.expect(transfer_model)
    def post(self):
        """Transfere valores entre carteiras"""
        data = request.json
        result = repo.transfer(data["from_wallet_id"], data["to_wallet_id"], data["amount"])
        if result is None:
            api.abort(400, "Insufficient balance or one of the wallets not found")
        return result, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
