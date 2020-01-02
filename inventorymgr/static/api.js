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

export function createQualification(qualification) {
    const params = createRequestParams(qualification);
    return fetch('/api/v1/qualifications', params);
}

export function updateQualification(qualification) {
    const params = updateRequestParams(qualification);
    return fetch('/api/v1/qualifications/' + qualification.id, params);
}

export function deleteQualification(qualification) {
    const headers = contentTypeJson();
    const params = {
        method: 'DELETE',
        headers,
        body: JSON.stringify(qualification),
    };
    return fetch('/api/v1/qualifications/' + qualification.id, params);
}

export function fetchQualifications() {
    return fetch('/api/v1/qualifications');
}

export function generateRegistrationToken() {
    const params = { method: 'POST' };
    return fetch('/api/v1/registration/tokens', params);
}

export function deleteRegistrationToken(token) {
    const params = { method: 'DELETE' };
    return fetch('/api/v1/registration/tokens/' + token.id, params);
}

export function fetchRegistrationTokens() {
    return fetch('/api/v1/registration/tokens');
}

export function fetchSessionUser() {
    return fetch('/api/v1/users/me');
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

export function fetchUsers() {
    return fetch('/api/v1/users');
}

export function login(user) {
    const params = createRequestParams(user);
    return fetch('/api/v1/auth/login', params);
}

export function logout() {
    const params = { method: 'POST' };
    return fetch('/api/v1/auth/logout', params);
}
