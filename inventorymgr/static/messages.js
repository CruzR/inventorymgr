export const messages = {
    en: {
        actions: {
            add: 'Add',
            cancel: 'Cancel',
            change_password: 'Change Password',
            checkin: 'Checkin',
            checkout: 'Checkout',
            copy: 'Copy',
            create: 'Create',
            create_item: 'Create Item',
            create_qualification: 'Create Qualification',
            create_user: 'Create User',
            delete: 'Delete',
            edit: 'Edit',
            generate_token: 'Generate Token',
            login: 'Login',
            logout: 'Logout',
            register: 'Register',
            save: 'Save',
            view: 'View',
        },
        errors: {
            already_borrowed: 'Item is already borrowed.',
            authentication_required: 'You need to be logged in to do that.',
            expired_token: 'Registration link has expired.',
            id_mismatch: 'IDs do not match.',
            id_specified: 'Cannot set an ID on creation.',
            incorrect_id: 'Incorrect ID.',
            insufficient_permissions: 'Insufficient permissions.',
            invalid_user_or_password: 'Invalid username or password.',
            invalid_token: 'Invalid registration link.',
            item_exists: 'Item already exists.',
            missing_fields: 'Required fields are missing.',
            missing_qualifications: 'User is missing required qualifications.',
            no_such_object: 'Object does not exist.',
            no_such_user: 'User does not exist.',
            nonexistent_item: 'Item does not exist.',
            object_exists: 'Object already exists.',
            password_mismatch: 'Passwords do not match.',
            password_missing: 'Password is missing.',
            permissions_not_subset: 'You cannot set permissions you do not have yourself.',
            qualification_exists: 'Qualification already exists.',
            unknown: 'An unknown error occurred during processing.',
            unknown_qualification: 'Qualification does not exist.',
            unknown_resource: 'Unknown API endpoint.',
            user_exists: 'User already exists.',
            validation_failed: 'API request was malformed, try refreshing the page.',
        },
        fields: {
            actions: 'Actions',
            barcode: 'Barcode',
            borrowed_by: 'Borrowed by',
            expires: 'Expires',
            item: 'Item',
            item_barcode: 'Item Barcode',
            new_password: 'New password',
            password: 'Password',
            permissions: 'Permissions',
            qualification: 'Qualification',
            qualifications: 'Qualifications',
            received_at: 'Received at',
            repeat_new_password: 'Repeat new password',
            repeat_password: 'Repeat password',
            required_qualifications: 'Required Qualifications',
            returned_at: 'Returned at',
            token: 'Token',
            user: 'User',
            user_barcode: 'User Barcode',
            username: 'Username',
        },
        page: {
            borrowed_items: 'Borrowed Items',
            checkin: 'Checkin',
            checkout: 'Checkout',
            inventory: 'Inventory',
            invites: 'Invites',
            qualifications: 'Qualifications',
            users: 'Users',
        },
        permissions: {
            create_users: 'Create Users',
            view_users: 'View Users',
            update_users: 'Edit Users',
            edit_qualifications: 'Edit Qualifications',
            create_items: 'Edit Inventory',
            manage_checkouts: 'Checkout Inventory',
        },
    },
    de: {
        actions: {
            add: 'Hinzufügen',
            cancel: 'Abbrechen',
            change_password: 'Passwort ändern',
            checkin: 'Annehmen',
            checkout: 'Ausgeben',
            copy: 'Kopieren',
            create: 'Erstellen',
            create_item: 'Objekt erstellen',
            create_qualification: 'Qualifikation erstellen',
            create_user: 'Benutzer erstellen',
            delete: 'Löschen',
            edit: 'Bearbeiten',
            generate_token: 'Token generieren',
            login: 'Anmelden',
            logout: 'Abmelden',
            register: 'Registrieren',
            save: 'Speichern',
            view: 'Anzeigen',
        },
        errors: {
            already_borrowed: 'Objekt ist bereits entliehen.',
            authentication_required: 'Du musst angemeldet sein, um das zu tun.',
            expired_token: 'Registrierungs-Link ist abgelaufen.',
            id_mismatch: 'IDs stimmen nicht überein.',
            id_specified: 'ID kann nicht beim Erstellen gesetzt werden.',
            incorrect_id: 'Falsche ID.',
            insufficient_permissions: 'Unzureichende Berechtigungen.',
            invalid_user_or_password: 'Benutzername oder Passwort ist falsch.',
            invalid_token: 'Ungültiger Registrierungs-Link.',
            item_exists: 'Objekt existiert bereits.',
            missing_fields: 'Pflichtfelder sind leer.',
            missing_qualifications: 'Benutzer hat nicht alle benötigten Qualifikationen.',
            no_such_object: 'Objekt existiert nicht.',
            no_such_user: 'Benutzer existiert nicht.',
            nonexistent_item: 'Objekt existiert nicht.',
            object_exists: 'Objekt existiert bereits.',
            password_mismatch: 'Passwörter stimmen nicht überein.',
            password_missing: 'Passwort fehlt.',
            permissions_not_subset: 'Du kannst keine Berechtigungen setzen, die du nicht selbst hast.',
            qualification_exists: 'Qualifikation existiert bereits.',
            unknown: 'Bei der Verarbeitung trat ein unbekannter Fehler auf.',
            unknown_qualification: 'Qualifikation existiert nicht.',
            unknown_resource: 'Unbekannter API-Endpoint.',
            user_exists: 'Benutzer existiert bereits.',
            validation_failed: 'API-Anfrage fehlgeschlagen, bitte Seite neu laden.',
        },
        fields: {
            actions: 'Aktionen',
            barcode: 'Barcode',
            borrowed_by: 'Ausgeliehen von',
            expires: 'Gültig bis',
            item: 'Objekt',
            item_barcode: 'Objekt-Barcode',
            new_password: 'Neues Passwort',
            password: 'Passwort',
            permissions: 'Berechtigungen',
            qualification: 'Qualifikation',
            qualifications: 'Qualifikationen',
            received_at: 'Erhalten am',
            repeat_new_password: 'Neues Paswort wiederholen',
            repeat_password: 'Passwort wiederholen',
            required_qualifications: 'Benötigte Qualifikationen',
            returned_at: 'Zurückgegeben am',
            token: 'Token',
            user: 'Benutzer',
            user_barcode: 'Benutzer-Barcode',
            username: 'Benutzername',
        },
        page: {
            borrowed_items: 'Entliehene Objekte',
            checkin: 'Annahme',
            checkout: 'Ausgabe',
            inventory: 'Inventar',
            invites: 'Einladungen',
            qualifications: 'Qualifikationen',
            users: 'Benutzer',
        },
        permissions: {
            create_users: 'Benutzer anlegen',
            view_users: 'Benutzer anzeigen',
            update_users: 'Benutzer bearbeiten',
            edit_qualifications: 'Qualifikationen bearbeiten',
            create_items: 'Inventar bearbeiten',
            manage_checkouts: 'Inventar ausgeben',
        },
    },
};
