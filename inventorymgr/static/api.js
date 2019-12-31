export function createItem(item) {
    const headers = new Headers();
    headers.append('Content-Type', 'application/json');
    const params = {
        method: 'POST',
        headers,
        body: JSON.stringify(item)
    };
    return fetch('/api/v1/items', params);
}
