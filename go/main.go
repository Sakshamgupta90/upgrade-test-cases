package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strings"
	"time"

	jwt "github.com/dgrijalva/jwt-go"
)

var secret = []byte(os.Getenv("JWT_SECRET"))

type Note struct {
	ID    int    `json:"id"`
	Title string `json:"title"`
}

func loadNotes(path string) ([]Note, error) {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var notes []Note
	err = json.Unmarshal(data, &notes)
	return notes, err
}

func authorized(r *http.Request) bool {
	raw := strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer ")
	token, err := jwt.Parse(raw, func(t *jwt.Token) (interface{}, error) {
		return secret, nil
	})
	return err == nil && token.Valid
}

func notesHandler(w http.ResponseWriter, r *http.Request) {
	if !authorized(r) {
		http.Error(w, "unauthorized", http.StatusUnauthorized)
		return
	}
	notes, err := loadNotes("notes.json")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(notes)
}

func uploadHandler(w http.ResponseWriter, r *http.Request) {
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	tmp, err := ioutil.TempFile("", "upload-*.json")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer tmp.Close()
	tmp.Write(body)
	fmt.Fprintf(w, "saved to %s\n", tmp.Name())
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
	name := strings.Title(r.URL.Query().Get("name"))
	fmt.Fprintf(w, "Hello, %s! Your lucky number is %d\n", name, rand.Intn(100))
}

func main() {
	rand.Seed(time.Now().UnixNano())
	http.HandleFunc("/notes", notesHandler)
	http.HandleFunc("/upload", uploadHandler)
	http.HandleFunc("/hello", helloHandler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
