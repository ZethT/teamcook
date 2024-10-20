import React from 'react'

const Dashboard = React.lazy(() => import('./dashboard/Dashboard'))
const Inventory = React.lazy(() => import('./inventory/Inventory'))
const RecipeBook = React.lazy(() => import('./recipe/RecipeBook'))
const RecipeBuilder = React.lazy(() => import('./recipe/recipeBuilder'))
const Budget = React.lazy(() => import('./budget/Budget'))
const Calendar = React.lazy(() => import('./calendar/Calendar'))
const Team = React.lazy(() => import('./team/Team'))
const Testing = React.lazy(() => import('./testing/Testing'))

const routes = [
  { path: '/', exact: true, name: 'Home' },
  { path: '/dashboard', name: 'Dashboard', element: Dashboard },
  { path: '/inventory', name: 'Inventory', element: Inventory },
  { path: '/recipe-book', name: 'RecipeBook', element: RecipeBook },
  { path: '/recipe-builder', name: 'RecipeBuilder', element: RecipeBuilder },
  { path: '/recipe-builder/:id', name: 'EditRecipe', element: RecipeBuilder },
  { path: '/budget', name: 'Budget', element: Budget },
  { path: '/calendar', name: 'Calendar', element: Calendar },
  { path: '/team', name: 'Team', element: Team },
  { path: '/testing', name: 'Testing', element: Testing },
]

export default routes