def is_expert(user):
    return user.groups.filter(name='Expert').exists()


def is_oper(user):
    return user.groups.filter(name='Oper').exists()