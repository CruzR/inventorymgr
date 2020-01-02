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

function isJsonResponse(response) {
    const contentType = response.headers.get('Content-Type');
    return contentType.split(';')[0].trim() === 'application/json';
}

function unpackJson(response) {
    if (response.ok) {
        return response.json().then(json => { return { success: true, data: json }; });
    } else if (isJsonResponse(response)) {
        return response.json().then(json => { return { success: false, error: json }; });
    } else {
        return {
            success: false,
            error: { reason: 'unknown', message: 'Error occurred during processing' }
        };
    }
}

export function createItem(item) {
    const params = createRequestParams(item);
    return fetch('/api/v1/items', params).then(unpackJson);
}

export function updateItem(item) {
    const params = updateRequestParams(item);
    return fetch('/api/v1/items/' + item.id, params).then(unpackJson);
}

export function deleteItem(item) {
    const params = { method: 'DELETE' };
    return fetch('/api/v1/items/' + item.id, params).then(unpackJson);
}

export function fetchItems(item) {
    return fetch('/api/v1/items');
}

export function createQualification(qualification) {
    const params = createRequestParams(qualification);
    return fetch('/api/v1/qualifications', params).then(unpackJson);
}

export function updateQualification(qualification) {
    const params = updateRequestParams(qualification);
    return fetch('/api/v1/qualifications/' + qualification.id, params).then(unpackJson);
}

export function deleteQualification(qualification) {
    const headers = contentTypeJson();
    const params = {
        method: 'DELETE',
        headers,
        body: JSON.stringify(qualification),
    };
    return fetch('/api/v1/qualifications/' + qualification.id, params).then(unpackJson);
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
    return fetch('/api/v1/users/me').then(unpackJson);
}

export function createUser(user) {
    const params = createRequestParams(user);
    return fetch('/api/v1/users', params).then(unpackJson);
}

export function updateUser(user_id, user) {
    const params = updateRequestParams(user);
    return fetch('/api/v1/users/' + user_id, params).then(unpackJson);
}

export function deleteUser(user_id) {
    const params = { method: 'DELETE' };
    return fetch('/api/v1/users/' + user_id, params).then(unpackJson);
}

export function fetchUsers() {
    return fetch('/api/v1/users').then(unpackJson);
}

export function login(user) {
    const params = createRequestParams(user);
    return fetch('/api/v1/auth/login', params);
}

export function logout() {
    const params = { method: 'POST' };
    return fetch('/api/v1/auth/logout', params);
}

export function register(token, user) {
    const params = createRequestParams(user);
    return fetch('/api/v1/auth/registration/' + token, params);
}
