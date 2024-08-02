import React from "react";
import { Button } from "react95";
import styled from "styled-components";

const ButtonWrapper = styled.div`
  margin: 0.5rem;
  display: flex;
  flex-direction: row-reverse;
`;

export default function AcceptButton({ acceptDataFun, type }) {
  return (
    <ButtonWrapper>
      <Button onClick={acceptDataFun} type={type}>
        Generuj
      </Button>
    </ButtonWrapper>
  );
}
