function contentTypeJson() {
    const headers = new Headers();
    headers.append('Content-Type', 'application/json');
    return headers;
}

function createRequestParams(obj) {
    const headers = contentTypeJson();
    const params = {
        method: 'POST',
        headers,
        body: JSON.stringify(obj)
    };
    return params;
}

function updateRequestParams(obj) {
    const headers = contentTypeJson();
    const params = {
        method: 'PUT',
        headers,
        body: JSON.stringify(obj),
    };
    return params;
}

export function createItem(item) {
    const params = createRequestParams(item);
    return fetch('/api/v1/items', params);
}

export function updateItem(item) {
    const params = updateRequestParams(item);
    return fetch('/api/v1/items/' + item.id, params);
}

export function deleteItem(item) {
    const params = { method: 'DELETE' };
    return fetch('/api/v1/items/' + item.id, params);
}

export function fetchItems(item) {
    return fetch('/api/v1/items');
}

export function createUser(user) {
    const params = createRequestParams(item);
    return fetch('/api/v1/users', params);
}

export function updateUser(user_id, user) {
    const params = updateRequestParams(user);
    return fetch('/api/v1/users/' + user_id, params);
}

export function deleteUser(user_id) {
    const params = { method: 'DELETE' };
    return fetch('/api/v1/users/' + user_id, params);
}
