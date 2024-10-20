import React from 'react'
import CIcon from '@coreui/icons-react'
import {
  cilSpeedometer,
  cilTruck,
  cilDinner,
  cilCalendar,
  cilChart,
  cilGroup,
  cilBeaker,
} from '@coreui/icons'
import { CNavGroup, CNavItem, CNavTitle } from '@coreui/react'

const _nav = [
  {
    component: CNavItem,
    name: 'Dashboard',
    to: '/dashboard',
    icon: <CIcon icon={cilSpeedometer} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Inventory',
    to: '/inventory',
    icon: <CIcon icon={cilTruck} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Recipe Book',
    to: '/recipe-book',
    icon: <CIcon icon={cilDinner} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Budget',
    to: '/budget',
    icon: <CIcon icon={cilChart} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Calendar',
    to: '/calendar',
    icon: <CIcon icon={cilCalendar} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Team',
    to: '/team',
    icon: <CIcon icon={cilGroup} customClassName="nav-icon" />,
  },

  {
    component: CNavItem,
    name: 'Testing',
    to: '/testing',
    icon: <CIcon icon={cilBeaker} customClassName="nav-icon" />,
  },
]

export default _nav
