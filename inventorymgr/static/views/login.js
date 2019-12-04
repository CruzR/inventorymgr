const template = `
    <div class="columns is-centered">
      <div class="column is-narrow">
        <h1 class="title">Login</h1>
        <div class="box">
        <div class="field">
          <label class="label">Username</label>
          <div class="control">
            <input class="input" type="text" placeholder="Username">
          </div>
        </div>
        <div class="field">
          <label class="label">Password</label>
          <div class="control">
            <input class="input" type="password" placeholder="Password">
          </div>
        </div>
        <div class="field">
          <div class="control">
            <button class="button is-primary">Login</button>
          </div>
        </div>
        </div>
      </div>
    </div>`

export default {
    template
}
