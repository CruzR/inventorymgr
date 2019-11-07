INSERT INTO users (username, password, view_users, update_user)
VALUES
    ('test', 'pbkdf2:sha256:150000$0cQjunn5$bdcc8358a53f42fb2dfc5a5a1e1dc5354228309c278f4c69cedeb300fc542610', TRUE, TRUE),
    ('min_permissions_user', 'pbkdf2:sha256:150000$0cQjunn5$bdcc8358a53f42fb2dfc5a5a1e1dc5354228309c278f4c69cedeb300fc542610', FALSE, FALSE);
