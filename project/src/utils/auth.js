import Cookies from 'js-cookie'
import cache from '@/plugins/cache'

const TokenKey = 'Admin-Token'

const ExpiresInKey = 'Admin-Expires-In'

const UserKey = 'Admin-User'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  const normalizedToken = token && token.startsWith('Bearer ')
    ? token.slice(7)
    : token
  return Cookies.set(TokenKey, normalizedToken)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function getExpiresIn() {
  return Cookies.get(ExpiresInKey) || -1
}

export function setExpiresIn(time) {
  return Cookies.set(ExpiresInKey, time)
}

export function removeExpiresIn() {
  return Cookies.remove(ExpiresInKey)
}

export function getUserInfo() {
  return cache.local.getJSON(UserKey)
}

export function setUserInfo(userInfo) {
  if (userInfo != null) {
    cache.local.setJSON(UserKey, userInfo)
  }
}

export function removeUserInfo() {
  cache.local.remove(UserKey)
}

export function clearAuth() {
  removeToken()
  removeExpiresIn()
  removeUserInfo()
}
