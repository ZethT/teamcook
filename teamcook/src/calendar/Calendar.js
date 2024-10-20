import React, { useState, useEffect } from 'react'
import {
  CCard,
  CCardHeader,
  CCardBody,
  CCardFooter,
  CButton,
  CRow,
  CCol,
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
  CForm,
  CFormInput,
  CFormLabel,
} from '@coreui/react'
import api from '../api'

const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date())
  const [selectedDate, setSelectedDate] = useState(new Date())
  const [view, setView] = useState('month') // 'month' or 'week'
  const [events, setEvents] = useState([])
  const [showModal, setShowModal] = useState(false)
  const [newEvent, setNewEvent] = useState('')

  useEffect(() => {
    fetchEvents()
  }, [currentDate, view])

  const fetchEvents = async () => {
    try {
      let startDate, endDate
      if (view === 'month') {
        startDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1)
        endDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0)
      } else {
        startDate = getWeekStart(currentDate)
        endDate = new Date(startDate)
        endDate.setDate(endDate.getDate() + 6)
      }
      const response = await api.get('/events/', {
        params: {
          start_date: startDate.toISOString(),
          end_date: endDate.toISOString(),
        },
      })
      setEvents(response.data)
    } catch (error) {
      console.error('Error fetching events:', error)
    }
  }

  const formatDate = (date) => {
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
  }

  const getWeekStart = (date) => {
    const d = new Date(date)
    const day = d.getDay()
    const diff = d.getDate() - day
    return new Date(d.setDate(diff))
  }

  const renderHeader = () => {
    if (view === 'month') {
      return (
        <CRow className="align-items-center">
          <CCol xs={2}>
            <CButton color="primary" onClick={prevMonth}>
              Previous
            </CButton>
          </CCol>
          <CCol xs={8} className="text-center">
            <h4>{currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}</h4>
          </CCol>
          <CCol xs={2} className="text-end">
            <CButton color="primary" onClick={nextMonth}>
              Next
            </CButton>
          </CCol>
        </CRow>
      )
    } else {
      const weekStart = getWeekStart(currentDate)
      const weekEnd = new Date(weekStart)
      weekEnd.setDate(weekEnd.getDate() + 6)
      return (
        <CRow className="align-items-center">
          <CCol xs={2}>
            <CButton color="primary" onClick={prevWeek}>
              Previous
            </CButton>
          </CCol>
          <CCol xs={8} className="text-center">
            <h4>
              {weekStart.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })} -
              {weekEnd.toLocaleDateString('en-US', {
                month: 'long',
                day: 'numeric',
                year: 'numeric',
              })}
            </h4>
          </CCol>
          <CCol xs={2} className="text-end">
            <CButton color="primary" onClick={nextWeek}>
              Next
            </CButton>
          </CCol>
        </CRow>
      )
    }
  }

  const onDateClick = (day) => {
    setSelectedDate(day)
  }

  const onDateDoubleClick = (day) => {
    setSelectedDate(day)
    setShowModal(true)
  }

  const nextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1))
  }

  const prevMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1))
  }

  const nextWeek = () => {
    const nextWeek = new Date(currentDate)
    nextWeek.setDate(currentDate.getDate() + 7)
    setCurrentDate(nextWeek)
  }

  const prevWeek = () => {
    const prevWeek = new Date(currentDate)
    prevWeek.setDate(currentDate.getDate() - 7)
    setCurrentDate(prevWeek)
  }

  const onAddEvent = async () => {
    if (newEvent.trim() !== '') {
      try {
        const eventData = {
          name: newEvent.trim(),
          time: selectedDate.toISOString(),
          // You might want to add created_by_id and restaurant_id here
        }
        await api.post('/events/', eventData)
        await fetchEvents() // Refresh events after adding a new one
        setNewEvent('')
        setShowModal(false)
      } catch (error) {
        console.error('Error adding event:', error)
      }
    }
  }

  const renderDays = () => {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    return (
      <CRow>
        {days.map((day) => (
          <CCol key={day} className="text-center fw-bold">
            {day}
          </CCol>
        ))}
      </CRow>
    )
  }

  const getEventsForDate = (date) => {
    return events.filter((event) => {
      const eventDate = new Date(event.time)
      return (
        eventDate.getFullYear() === date.getFullYear() &&
        eventDate.getMonth() === date.getMonth() &&
        eventDate.getDate() === date.getDate()
      )
    })
  }

  const renderCells = () => {
    const monthStart = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1)
    const monthEnd = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0)
    const startDate = new Date(monthStart)
    startDate.setDate(startDate.getDate() - startDate.getDay())
    const endDate = new Date(monthEnd)
    endDate.setDate(endDate.getDate() + (6 - endDate.getDay()))

    const rows = []
    let days = []
    let day = new Date(startDate)

    while (day <= endDate) {
      for (let i = 0; i < 7; i++) {
        const cloneDay = new Date(day)
        const formattedDate = day.getDate()
        const dateEvents = getEventsForDate(day)
        days.push(
          <CCol
            key={day}
            className={`p-2 border ${
              day.getMonth() !== currentDate.getMonth()
                ? 'text-muted'
                : day.toDateString() === selectedDate.toDateString()
                  ? 'bg-primary text-white'
                  : ''
            }`}
            onClick={() => onDateClick(cloneDay)}
            onDoubleClick={() => onDateDoubleClick(cloneDay)}
          >
            <div>{formattedDate}</div>
            {dateEvents.length > 0 && (
              <div className="small mt-1">
                {dateEvents.map((event, index) => (
                  <div key={index} className="text-truncate">
                    {event.name}
                  </div>
                ))}
              </div>
            )}
          </CCol>,
        )
        day.setDate(day.getDate() + 1)
      }
      rows.push(
        <CRow key={day} className="g-0">
          {days}
        </CRow>,
      )
      days = []
    }
    return <div className="mt-2">{rows}</div>
  }

  const renderWeekView = () => {
    const weekStart = getWeekStart(currentDate)
    const days = []

    for (let i = 0; i < 7; i++) {
      const cloneDay = new Date(weekStart)
      cloneDay.setDate(weekStart.getDate() + i)
      const dateEvents = getEventsForDate(cloneDay)
      days.push(
        <CCol
          key={i}
          className={`p-2 border ${
            cloneDay.toDateString() === selectedDate.toDateString() ? 'bg-primary text-white' : ''
          }`}
          onClick={() => onDateClick(cloneDay)}
          onDoubleClick={() => onDateDoubleClick(cloneDay)}
        >
          <div>{cloneDay.toLocaleDateString('en-US', { weekday: 'short', day: 'numeric' })}</div>
          {dateEvents.length > 0 && (
            <div className="small mt-1">
              {dateEvents.map((event, index) => (
                <div key={index} className="text-truncate">
                  {event.name}
                </div>
              ))}
            </div>
          )}
        </CCol>,
      )
    }
    return <CRow className="g-0 mt-2">{days}</CRow>
  }

  return (
    <>
      <CCard className="mb-4">
        <CCardHeader>
          {renderHeader()}
          <CRow className="mt-2">
            <CCol xs={6}>
              <CButton
                color={view === 'month' ? 'primary' : 'secondary'}
                onClick={() => setView('month')}
                className="me-2"
              >
                Month
              </CButton>
              <CButton
                color={view === 'week' ? 'primary' : 'secondary'}
                onClick={() => setView('week')}
              >
                Week
              </CButton>
            </CCol>
          </CRow>
        </CCardHeader>
        <CCardBody>
          {renderDays()}
          {view === 'month' ? renderCells() : renderWeekView()}
        </CCardBody>
        <CCardFooter>
          <p>Selected Date: {formatDate(selectedDate)}</p>
          <p>Double-click a date to add an event</p>
        </CCardFooter>
      </CCard>

      <CModal visible={showModal} onClose={() => setShowModal(false)}>
        <CModalHeader closeButton>
          <CModalTitle>Add Event for {formatDate(selectedDate)}</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <CForm>
            <CFormLabel htmlFor="newEvent">Event Details</CFormLabel>
            <CFormInput
              id="newEvent"
              placeholder="Enter event details"
              value={newEvent}
              onChange={(e) => setNewEvent(e.target.value)}
            />
          </CForm>
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={() => setShowModal(false)}>
            Close
          </CButton>
          <CButton color="primary" onClick={onAddEvent}>
            Add Event
          </CButton>
        </CModalFooter>
      </CModal>
    </>
  )
}

export default Calendar
