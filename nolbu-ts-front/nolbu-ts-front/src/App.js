import React, { useState } from "react";
import { sendFormData } from "./api.js";
import "./App.css";
import { createGlobalStyle, ThemeProvider } from "styled-components";
import RowInput from "./components/RowInput.js";
import ListInput from "./components/ListInput.js";
import AcceptButton from "./components/AcceptButton.js";
import { useForm } from "react-hook-form";
import { Window, WindowHeader, Separator, styleReset } from "react95";

/* Pick a theme of your choice */
import original from "react95/dist/themes/original";

import ms_sans_serif from "react95/dist/fonts/ms_sans_serif.woff2";
import ms_sans_serif_bold from "react95/dist/fonts/ms_sans_serif_bold.woff2";

const GlobalStyles = createGlobalStyle`
  ${styleReset}
  @font-face {
    font-family: 'ms_sans_serif';
    src: url('${ms_sans_serif}') format('woff2');
    font-weight: 400;
    font-style: normal
  }
  @font-face {
    font-family: 'ms_sans_serif';
    src: url('${ms_sans_serif_bold}') format('woff2');
    font-weight: bold;
    font-style: normal
  }
  body, input, select, textarea {
    font-family: 'ms_sans_serif';
  }
`;

export default function App() {
  const { register, handleSubmit } = useForm();
  const onSubmit = (data) => sendFormData(data);

  return (
    <div>
      <GlobalStyles />
      <ThemeProvider theme={original}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <Window className="window">
            <WindowHeader className="window-title">
              <span>Nolbu TS (alpha 1.0)</span>
            </WindowHeader>
            <div className="contentDiv">
              <div className="labelsDiv">
                <RowInput
                  labelValue="Miesiac"
                  rowInputType="number"
                  register={register}
                  registerName="month"
                />
                <RowInput
                  labelValue="Rok"
                  rowInputType="number"
                  register={register}
                  registerName="year"
                />
                <RowInput
                  labelValue="Liczba Godzin"
                  rowInputType="number"
                  register={register}
                  registerName="numberOfHours"
                />
                <RowInput
                  labelValue="Imie Nazwisko"
                  rowInputType="text"
                  register={register}
                  registerName="userName"
                />
                <RowInput
                  labelValue="Projekt"
                  rowInputType="text"
                  register={register}
                  registerName="projectName"
                />
              </div>
            </div>
            <div>
              <ListInput
                label="Lista zadan (przynajmniej z 5, wymienione po przecinku):"
                register={register}
                registerName="tasks"
              />
            </div>
            <Separator />
            <AcceptButton type="submit" />
          </Window>
        </form>
      </ThemeProvider>
    </div>
  );
}
