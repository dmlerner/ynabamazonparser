from ynab_sdk import YNAB

import ynabassistant as ya

api = YNAB(ya.settings.api_key)


def get_all_transactions():
    ya.utils.log_debug('get_all_transactions')
    response = api.transactions.get_transactions(ya.settings.budget_id)
    raw = response.data.transactions
    transactions = list(map(ya.ynab.transaction.Transaction, raw))
    ya.utils.log_info('Found %s transactions' % len(transactions or []))
    transactions.sort(key=lambda t: t.date, reverse=True)
    return ya.utils.by(transactions, lambda t: t.id)


def update_all(transactions):
    ya.utils.log_debug('update_all')
    for t in transactions:
        update(t)


def update(t):
    ya.utils.log_debug('update', t)
    s = t.subtransactions
    t.subtransactions = []
    p = t.to_parent()
    response = api.transactions.update_transaction(ya.settings.budget_id, p)
    if 'error' in response:
        ya.utils.log_error('ERROR:', response)
        return
    t.subtransactions = s


def create(transactions):
    ya.utils.log_debug('create', *transactions)
    transaction_requests = [t.to_transaction_request() for t in transactions]
    response = api.transactions.create_transactions(ya.settings.budget_id, transaction_requests)
    ya.utils.log_debug('response', response)
    if 'error' in response:
        ya.utils.log_error('ERROR:', response)


def get_categories():
    response = api.categories.get_categories(ya.settings.budget_id)
    groups = response.data.category_groups
    categories = []
    for g in groups:
        for c in g.categories:
            categories.append(ya.ynab.category.Category(c, g.name))
    return ya.utils.by(categories, lambda c: c.id)
