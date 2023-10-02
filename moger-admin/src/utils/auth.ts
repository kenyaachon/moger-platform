import { Auth } from 'aws-amplify'

export async function userLoggedIn() {
  try {
    const data = await Auth.currentSession()
    console.log(data)
    return true
  } catch (error) {
    console.log(error)
    return false
  }
}
