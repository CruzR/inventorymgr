function contentTypeJson() {
    const headers = new Headers();
    headers.append('Content-Type', 'application/json');
    return headers;
}

export function createItem(item) {
    const headers = contentTypeJson();
    const params = {
        method: 'POST',
        headers,
        body: JSON.stringify(item)
    };
    return fetch('/api/v1/items', params);
}

export function updateItem(item) {
    const headers = contentTypeJson();
    const params = {
        method: 'PUT',
        headers,
        body: JSON.stringify(item),
    };
    return fetch('/api/v1/items/' + item.id, params);
}

export function deleteItem(item) {
    const params = { method: 'DELETE' };
    return fetch('/api/v1/items/' + item.id, params);
}
