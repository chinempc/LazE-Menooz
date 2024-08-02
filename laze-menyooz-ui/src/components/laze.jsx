"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"
import { Input } from "@/components/ui/input"

export default function LazE() {
  const [schoolName, setSchoolName] = useState("")
  const [foodItem, setFoodItem] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [response, setResponse] = useState("")
  const [isDarkMode, setIsDarkMode] = useState(true)
  const schools = ["UMES"]
  const handleSubmit = async (e) => {
    e.preventDefault()
    if (schoolName.trim() === "" || foodItem.trim() === "") {
      setResponse("Please enter a school name and a food item.")
      return
    }
    setIsLoading(true)
    try {
        const transformData = (data) => {
            let dataLength = data.length
            let daysServed = ""
            let andFlag = dataLength > 1

            if (dataLength == 1) {
              if (data[0].served == false) {
                return data[0].message
              } else {
                return `${foodItem} will be served for ${data[0].serving_period} on ${data[0].serving_day} this week 😃🍽️!!!`
              }
            }

            for (let i = 0; i < dataLength; i++) {
              if (i == dataLength-1 && andFlag) {
                daysServed += `and ${data[i].serving_period} on ${data[i].serving_day} `
              } else {
                daysServed += `${data[i].serving_period} on ${data[i].serving_day}, `
              }
            }

            return `${foodItem} will be served for ${daysServed} this week 😃🍽️!!!`
        }

      //console.log(foodItem)
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/${foodItem}`)
      if (!res.ok) {
        //console.log(res)
        throw new Error("Network response was not ok!")
      }
      
      const data = await res.json()
      //console.log(data)
      setResponse(transformData(data))
    } catch (error) {
        //console.log("Error fetching data: ", error)
        setResponse("Error fetching data. Please try again later.")
    } finally {
      setIsLoading(false)
    }
  }
  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => !prevMode)
  }
  return (
    <div
      className={`flex flex-col items-center min-h-screen ${
        isDarkMode ? "bg-background-dark text-foreground-dark" : "bg-foreground text-background"
      }`}
    >
      <header className="w-full max-w-md py-6 px-4 border-b">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <BeefIcon className={`h-8 w-8 ${isDarkMode ? "text-primary" : "text-primary-dark"}`} />
            <span className="text-2xl font-bold"> LazE Menyooz</span>
          </div>
          <button
            onClick={toggleDarkMode}
            className={`p-2 rounded-full transition-colors ${
              isDarkMode
                ? "bg-primary-dark text-primary-foreground-dark hover:bg-primary-dark/90"
                : "bg-primary text-primary-foreground hover:bg-primary/90"
            }`}
          >
            {isDarkMode ? <MoonIcon className="h-6 w-6" /> : <SunIcon className="h-6 w-6" />}
          </button>
        </div>
      </header>
      <br />
      <main className="w-full max-w-md p-6 space-y-6">
        <div className="text-center">
          Welcome to LazE Menyooz your go-to solution for staying updated on your favorite dishes!
        </div>
        <div className="flex justify-center space-x-4">
          <a href="">
            <Button variant="ghost" size="icon">
              <GlobeIcon className="h-6 w-6" />
            </Button>
          </a>
          <a href="https://github.com/chinempc">
            <Button variant="ghost" size="icon">
              <GitlabIcon className="h-6 w-6" />
            </Button>
          </a>
        </div>
        <hr className="border-muted" />
        <br /><br />
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="school-name">School Name</Label>
            <Select
              value={schoolName}
              onValueChange={setSchoolName}
              className={`bg-input rounded-md ${isDarkMode ? "text-foreground-dark" : "text-white"}`}
            >
              <SelectTrigger className={`bg-input ${isDarkMode ? "text-foreground-dark" : "text-white"}`}>
                <SelectValue placeholder="Select a school" />
              </SelectTrigger>
              <SelectContent className={`bg-input ${isDarkMode ? "text-foreground-dark" : "text-white"}`}>
                {schools.map((school) => (
                  <SelectItem key={school} value={school}>
                    {school}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="food-item">Favorite Food</Label>
            <Input
              id="food-item"
              type="text"
              placeholder="Enter your favorite food"
              value={foodItem}
              onChange={(e) => setFoodItem(e.target.value)}
              className={`bg-input placeholder:text-muted-foreground/50 ${
                isDarkMode ? "text-foreground-dark" : "text-white"
              }`}
            />
          </div>
          <Button
            type="submit"
            className={`w-full ${
              isDarkMode
                ? "bg-primary text-primary-foreground hover:bg-primary/90"
                : "bg-black text-white hover:bg-gray-800"
            }`}
          >
            {isLoading ? (
              <div className={`h-8 w-8 animate-spin ${isDarkMode ? "text-primary-dark" : "text-primary"}`} />
            ) : (
              "Check Availability"
            )}
          </Button>
        </form>
        {response && (
          <div className={`text-center ${isDarkMode ? "text-foreground-dark" : "text-background"}`}>{response}</div>
        )}
      </main>
    </div>
  )
}

function BeefIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12.5" cy="8.5" r="2.5" />
      <path d="M12.5 2a6.5 6.5 0 0 0-6.22 4.6c-1.1 3.13-.78 3.9-3.18 6.08A3 3 0 0 0 5 18c4 0 8.4-1.8 11.4-4.3A6.5 6.5 0 0 0 12.5 2Z" />
      <path d="m18.5 6 2.19 4.5a6.48 6.48 0 0 1 .31 2 6.49 6.49 0 0 1-2.6 5.2C15.4 20.2 11 22 7 22a3 3 0 0 1-2.68-1.66L2.4 16.5" />
    </svg>
  )
}


function GitlabIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m22 13.29-3.33-10a.42.42 0 0 0-.14-.18.38.38 0 0 0-.22-.11.39.39 0 0 0-.23.07.42.42 0 0 0-.14.18l-2.26 6.67H8.32L6.1 3.26a.42.42 0 0 0-.1-.18.38.38 0 0 0-.26-.08.39.39 0 0 0-.23.07.42.42 0 0 0-.14.18L2 13.29a.74.74 0 0 0 .27.83L12 21l9.69-6.88a.71.71 0 0 0 .31-.83Z" />
    </svg>
  )
}


function GlobeIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20" />
      <path d="M2 12h20" />
    </svg>
  )
}


function MoonIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" />
    </svg>
  )
}


function SunIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2" />
      <path d="M12 20v2" />
      <path d="m4.93 4.93 1.41 1.41" />
      <path d="m17.66 17.66 1.41 1.41" />
      <path d="M2 12h2" />
      <path d="M20 12h2" />
      <path d="m6.34 17.66-1.41 1.41" />
      <path d="m19.07 4.93-1.41 1.41" />
    </svg>
  )
}