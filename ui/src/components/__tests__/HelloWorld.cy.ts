import TheWelcome from '../TheWelcome.vue'

describe('TheWelcome', () => {
  it('playground', () => {
    cy.mount(TheWelcome, { props: { msg: 'Welcome' } })
  })

  it('renders properly', () => {
    cy.mount(TheWelcome, { props: { msg: 'Welcome' } })
    cy.get('h1').should('contain', 'Welcome')
  })
})
